import os
import jwt
from jwt.exceptions import InvalidTokenError
from models import *
from pwdlib import PasswordHash
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import case
from datetime import datetime, timezone, timedelta

ACCESS_TOKEN_EXPIRY_MINS = 30 # 30 mins
SECRET_KEY = "0799e0684381417197801be91edc072ebd87d699d5784b2ca9b3818cca8dec57"
ALGORITHM = "HS256"
password_hasher = PasswordHash.recommended()
roles = ("user", "admin", "librarian")
advanced_roles = roles[1:]

def generate_access_token(username):
    data = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINS)}
    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def decode_access_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return False
    return data

def encrypt_password(password):
    password_hash = password_hasher.hash(password)
    return password_hash

def verify_password(plaintext_password, password_hash):
    if not password_hasher.verify(
        plaintext_password, password_hash):
        return False
    return True

class LibraryDB:
    def __init__(self, file="library.db", backup_file="backups.db"):
        self.initialize_databases(file, backup_file)

    def initialize_databases(self, file, backup_file):
        if not os.path.isfile(file) and os.path.isfile(backup_file):
            self.create_database(file)
            self.create_backup_database(backup_file)
            self.restore_backup()
            print("Successfully restored database from backup!")
            return
        self.create_database(file)
        self.create_backup_database(backup_file)
        print("Successfully created / connected to the database!")

    def create_database(self, file):
        self.db = create_engine(f"sqlite+pysqlite:///{file}")
        self.raw_db = self.db.raw_connection()
        self.session = Session(self.db)
        self.create_table()

    def create_backup_database(self, backup_file):
        self.backup_db = sqlite3.connect(backup_file, check_same_thread=False)

    def restore_backup(self):
        self.backup_db.backup(self.raw_db.driver_connection)

    def create_table(self):
        Base.metadata.create_all(self.db)

    def user_result_to_account_response(self, query_result):
        if not query_result:
            return None
        response = UserResponse(
            id=query_result.id,
            username=query_result.username,
            role=query_result.role
        )
        return response

    def users_results_to_accounts_response(self, query_results):
        responses = [
                self.user_result_to_account_response(query_result)
                for query_result in query_results
        ]
        return responses

    def get_user_by_token(self, token):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        return user

    def get_user(self, token, user_id):
        user = self.get_user_by_token(token)
        if not (user.role in advanced_roles):
            return False
        user_result = self.session.get(User, user_id)
        if not user_result:
            return None
        response = self.user_result_to_account_response(user_result)
        return response

    def get_users(self, token):
        user = self.get_user_by_token(token)
        if not (user.role in advanced_roles):
            return False
        query = select(User.id, User.username, User.role)
        results = self.session.execute(query).all()
        responses = self.users_results_to_accounts_response(results)
        return responses


    def modify_user_role(self, token, user_id, new_role):
        user = self.get_user_by_token(token)
        if user.role != "admin":
            return False
        if not (new_role in roles):
            return None
        result = self.session.get(User, user_id)
        if not result:
            return None
        result.role = new_role
        return self.user_result_to_account_response(result)

    def get_user_by_name(self, username):
        user_query = select(User).where(
            User.username == username
        )
        try:
            result = self.session.execute(user_query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            return None
        return result

    def add_user(self, creation_details: UserCreationRequest):
        user = self.get_user_by_name(creation_details.username)
        if user:
            return False
        new_user = User(
            username=creation_details.username,
            password_hash=encrypt_password(
                creation_details.password
            ),
            role="user"
        )
        self.session.add(new_user)
        self.save_data()
        response = UserCreationResponse(
            username=creation_details.username,
            fullname=creation_details.fullname
        )
        return response

    def filter_books(self, token, author=None, title=None, year=None,
        available=None, pages=None, min_pages=None, max_pages=None,
        sort_by=None, order=None, limit=0, offset=0):
        user = self.get_user_by_token(token)
        query = select(Books).where(
            and_(
                Books.user_id == user.id,
                Books.deleted_at == None
            )
        )
        if author:
            query = query.where(Books.author == author)

        if title:
            query = query.where(Books.title == title)

        if year:
            query = query.where(Books.year == year)

        if available is not None:
            query = query.where(Books.available == available)

        if pages:
            query = query.where(Books.pages == pages)

        if min_pages:
            query = query.where(Books.pages >= min_pages)

        if max_pages:
            query = query.where(Books.pages <= max_pages)
       
        if order:
            order = order.lower()

        should_sort = False
        if sort_by == "title":
            field_order = Books.title.desc() if order == "desc" else Books.title
            should_sort = True
        elif sort_by == "pages":
            field_order = Books.pages.desc() if order == "desc" else Books.pages
            should_sort = True
        elif sort_by == "year":
            field_order = Books.year.desc() if order == "desc" else Books.year
            should_sort = True
        
        if should_sort:
            query = query.order_by(field_order, Books.id.desc() if order == "desc" else Books.id)

        if limit and limit > 0:
            query = query.limit(limit)

        if offset and offset > 0:
            query = query.offset(offset)

        results = self.session.execute(query).all()
        results = self.query_results_to_book_responses(results)
        return results 

    def get_books(self, token, all_books=False):
        user = self.get_user_by_token(token)
        if not all_books:
            results = self.session.execute(
                select(Books).where(
                    and_(
                        Books.user_id == user.id,
                        Books.deleted_at == None
                    )
                )
            ).all()
        elif all_books and user.role in advanced_roles:
            results = self.session.execute(
                select(Books)
            ).all()
        elif all_books:
            return False
        book_responses = self.query_results_to_book_responses(results)
        return book_responses

    def get_book_by_id(self, token, book_id):
        user = self.get_user_by_token(token)
        if user.role == "user":
            query = select(Books).where(
                and_(
                    Books.id == book_id,
                    Books.user_id == user.id,
                    Books.deleted_at == None
                )
            )
        elif user.role in advanced_roles:
            query = select(Books).where(
                Books.id == book_id
            )
        try:
            result = self.session.execute(query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            result = None
        book_response = self.query_result_to_book_response(result)
        return book_response

    def query_result_to_book_response(self, query_result):
        if not query_result:
            return None
        book_response = BookResponse(
                id=query_result.id,
                user_id=query_result.user_id,
                title=query_result.title,
                author=query_result.author,
                year=query_result.year,
                pages=query_result.pages,
                available=query_result.available,
                created_at=query_result.created_at,
                updated_at=query_result.updated_at,
                deleted_at=query_result.deleted_at
        )
        return book_response
    
    def query_results_to_book_responses(self, query_results):
        book_responses = [
            self.query_result_to_book_response(query_result[0])
            for query_result in query_results
        ]
        return book_responses

    def get_book_count(self, token):
        user = self.get_user_by_token(token)

        query = select(func.count(Books.id).label("book_count")).where(
            and_(
                Books.user_id == user.id,
                Books.deleted_at == None
            )
        )
        result = self.session.execute(query).first()
        return result.book_count or 0

    def get_book_stats(self, token):
        user = self.get_user_by_token(token)
        query = select(
            func.count(Books.id).label("total_books"),
            func.count(case((Books.available == True, 1))).label("available_books"),
            func.count(case((Books.available == False, 1))).label("unavailable_books")
        ).where(
            and_(
                Books.user_id == user.id,
                Books.deleted_at == None
            )
        )
        result = self.session.execute(query).first() 
        return {
            "total_books": result.total_books or 0,
            "available_books": result.available_books or 0,
            "unavailable_books": result.unavailable_books or 0,
        }

    def get_latest_book(self, token):
        user = self.get_user_by_token(token)

        query = select(Books).where(
            and_(
                Books.user_id == user.id,
                Books.deleted_at == None
            )
        ).order_by(Books.year.desc())
        result = self.session.execute(query).first()
        if result:
            result = self.query_result_to_book_response(result[0])
        return result
    
    def get_available_books(self, token):
        available_books = self.filter_books(token, available=True)
        return available_books

    def get_unavailable_books(self, token):
        unavailable_books = self.filter_books(token, available=False)
        return unavailable_books

    def add_book(self, token, book_details: BookCreationRequest):
        user = self.get_user_by_token(token)
        if user.role == "user":
            new_book = Books(
                user_id=user.id,
                title=book_details.title,
                author=book_details.author,
                year=book_details.year,
                pages=book_details.pages,
                available = True,
                created_at = datetime.now()
            )
        elif user.role in advanced_roles:
            id_selected = user.id if book_details.user_id is None else book_details.user_id
            new_book = Books(
                user_id=id_selected,
                title=book_details.title,
                author=book_details.author,
                year=book_details.year,
                pages=book_details.pages,
                available = True,
                created_at = datetime.now()
            )
        self.session.add(new_book)
        self.save_data()
        book_response = self.query_result_to_book_response(new_book)
        return book_response

    def remove_book(self, token, book_id):
        user = self.get_user_by_token(token)
        if user.role == "user":
            query = select(Books).where(
                and_(
                    Books.id == book_id,
                    Books.user_id == user.id,
                    Books.deleted_at == None
                )
            )
        elif user.role in advanced_roles:
            query = select(Books).where(
                Books.id == book_id
            )
        try:
            book = self.session.execute(query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            book = None
        if book:
            book.deleted_at = datetime.now()
        book_response = self.query_result_to_book_response(book)
        self.save_data()
        return book_response

    def update_book(self, token, book_id, book_details: BookUpdateRequest):
        user = self.get_user_by_token(token)
        updated = False

        if user.role == "user":
            query = select(Books).where(
                and_(
                    Books.id == book_id,
                    Books.user_id == user.id,
                    Books.deleted_at == None
                )
            )
        elif user.role in advanced_roles:
            query = select(Books).where(
                Books.id == book_id
            )

        try:
            book = self.session.execute(query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            book = None
        if book:
            if book_details.title:
                book.title = book_details.title
                updated = True

            if book_details.author:
                book.author = book_details.author
                updated = True

            if book_details.year:
                book.year = book_details.year
                updated = True

            if book_details.pages:
                book.pages = book_details.pages
                updated = True

            if book_details.available is not None:
                book.available = book_details.available
                updated = True
            
            if updated:
                book.updated_at = datetime.now()
                self.save_data()
        return self.query_result_to_book_response(book)

    def restore_book(self, token, book_id):
        user = self.get_user_by_token(token)
        if user.role not in advanced_roles:
            return False
        book = self.session.get(Books, book_id)
        if not book:
            return None
        if book.deleted_at:
            book.deleted_at = None
            self.save_data()
        else:
            return None
        return self.query_result_to_book_response(book)

    def save_data(self):
        self.session.commit()
        self.raw_db.backup(self.backup_db)

    def close(self):
        self.session.close()
        self.raw_db.close()
