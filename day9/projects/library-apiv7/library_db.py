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
            )
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
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        query = select(Books).where(Books.user_id == user.id)
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

    def get_books(self, token):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        results = self.session.execute(select(Books).where(Books.user_id == user.id)).all()
        book_responses = self.query_results_to_book_responses(results)
        return book_responses

    def get_book_by_id(self, token, book_id):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        query = select(Books).where(
            and_(
                Books.id == book_id,
                Books.user_id == user.id
            )
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
                title=query_result.title,
                author=query_result.author,
                year=query_result.year,
                pages=query_result.pages,
                available=query_result.available
        )
        return book_response
    
    def query_results_to_book_responses(self, query_results):
        book_responses = [
            self.query_result_to_book_response(query_result[0])
            for query_result in query_results
        ]
        return book_responses

    def get_book_count(self, token):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])

        query = select(func.count(Books.id).label("book_count")).where(Books.user_id == user.id)
        result = self.session.execute(query).first()
        return result.book_count or 0

    def get_book_stats(self, token):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        query = select(
            func.count(Books.id).label("total_books"),
            func.count(case((Books.available == True, 1))).label("available_books"),
            func.count(case((Books.available == False, 1))).label("unavailable_books")
        ).where(Books.user_id == user.id)
        result = self.session.execute(query).first() 
        return {
            "total_books": result.total_books or 0,
            "available_books": result.available_books or 0,
            "unavailable_books": result.unavailable_books or 0,
        }

    def get_latest_book(self, token):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])

        query = select(Books).where(Books.user_id == user.id).order_by(Books.year.desc())
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
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])

        new_book = Books(
            user_id=user.id,
            title=book_details.title,
            author=book_details.author,
            year=book_details.year,
            pages=book_details.pages,
            available = True
        )
        self.session.add(new_book)
        self.save_data()
        book_response = self.query_result_to_book_response(new_book)
        return book_response

    def remove_book(self, token, book_id):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])
        query = select(Books).where(
            and_(
                Books.id == book_id,
                Books.user_id == user.id
            )
        )
        try:
            book = self.session.execute(query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            book = None
        if book:
            self.session.delete(book)
        book_response = self.query_result_to_book_response(book)
        self.save_data()
        return book_response

    def update_book(self, token, book_id, book_details: BookUpdateRequest):
        decoded_token = decode_access_token(token)
        if not decoded_token:
            raise InvalidTokenError
        user = self.get_user_by_name(decoded_token["sub"])

        updated = False
        query = select(Books).where(
            and_(
                Books.id == book_id,
                Books.user_id == user.id
            )
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
                self.save_data()
        return self.query_result_to_book_response(book)

    def save_data(self):
        self.session.commit()
        self.raw_db.backup(self.backup_db)

    def close(self):
        self.session.close()
        self.raw_db.close()
