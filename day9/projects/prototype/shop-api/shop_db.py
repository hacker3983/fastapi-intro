import os
import jwt
import sqlite3
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.models import *

# Generate 32 bytes jwt key using openssl rand -hex 32
SECRET_KEY = "741cd06f6e55b1096f657dadda4945c50a21ada5e9e6b785f90d4b11f9b585b2"
ALGORITHM = "HS256" # Algorithm to use to generate JWT token
password_hasher = PasswordHash.recommended() # Intilialize password hashing object to use ARGON2 algorithm or recommnded hashing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def encrypt_password(password):
    return password_hasher.hash(password)

def verify_password(password, hashed_password):
    return password_hasher.verify(password, hashed_password)

def generate_access_token(username, expires_delta: timedelta | None = None):
    data = {"sub": username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.update({"exp": expire})
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

class ProductExistsError(Exception):
    "The product already exists!"

class ShopDB:
    def __init__(self, file="shop.db", backup_file="backups.db"):
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

    def product_to_response_model(self, product):
        response = ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                value=product.value
        )
        return response

    def query_results_to_response_models(self, results):
        responses = [self.product_to_response_model(result[0]) for result in results]
        return responses 

    def get_user_by_token(self, token):
        user_query = select(User).where(User.access_token == token)
        try:
            response = self.session.execute(user_query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            response = None
        return response

    def get_user_by_name(self, username):
        user_query = select(User).where(User.username == username)
        try:
            response = self.session.execute(user_query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            response = None
        return response


    def add_user(self, user_details: UserCreationRequest):
        user_query = select(User).where(User.username == user_details.username)
        try:
            result = self.session.execute(user_query).scalar_one()
            if result:
                return None
        except sqlalchemy.exc.NoResultFound:
            pass
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_user = User(
                username=user_details.username,
                full_name=user_details.full_name,
                password_hash=encrypt_password(user_details.password),
                access_token=generate_access_token(user_details.username, expires_delta=token_expires)
        )
        self.session.add(new_user)
        self.save_data()
        response = UserCreationResponse(
            data=UserCreationDetails(
                username=user_details.username,
                full_name=user_details.full_name
            )
        )
        return response

    def add_product(self, token, product_details: ProductCreationRequest):
        user = self.get_user_by_token(token)
        if not user:
            return None
        product_query = select(Product).where(
                and_(
                    Product.name == product_details.name,
                    Product.user_id == user.id
                )
        )
        try:
            result = self.session.execute(product_query).scalar_one()
            if result:
                return False
        except sqlalchemy.exc.NoResultFound:
            pass
        new_product = Product(
                user_id=user.id,
                name=product_details.name,
                description=product_details.description,
                value=product_details.value
        )
        self.session.add(new_product)
        self.save_data()
        response = ProductCreationResponse(
            data = self.product_to_response_model(new_product)
        )
        return response

    def get_product_count(self, token):
        user = self.get_user_by_token(token)
        if not user:
            return False
        query = select(
                    func.count(Product.id)
                ).where(
                    Product.user_id == user.id
                )
        result = self.session.execute(query).scalar_one()
        response = ProductCountResponse(product_count=result)
        return response

    def get_products(self, token):
        user = self.get_user_by_token(token)
        if not user:
            return False
        query = select(Product).where(Product.user_id == user.id)
        results = self.session.execute(query).all()
        responses = self.query_results_to_response_models(results)
        return responses

    def get_product(self, token, product_id):
        user = self.get_user_by_token(token)
        if not user:
            return False
        query = select(Product).where(
                and_(
                    Product.user_id == user.id,
                    Product.id == product_id
                )
        )
        try:
            product = self.session.execute(query).scalar_one()
            response = self.product_to_response_model(product)
        except sqlalchemy.exc.NoResultFound:
            response = None
        return response
    
    def update_product(self, token, product_id, product_details: ProductUpdateRequest):
        user = self.get_user_by_token(token)
        if not user:
            return False
        product_query = select(Product).where(
                and_(
                    Product.user_id == user.id,
                    Product.id == product_id
                )
        )
        try: 
            products = self.get_products(token)
            product = self.session.execute(product_query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            return None
        updated = False
        if product_details.name:
            for my_product in products:
                if my_product.name == product_details.name:
                    raise ProductExistsError
            product.name = product_details.name
            updated = True
        if product_details.description:
            product.description = product_details.description
            updated = True
        if product_details.value is not None:
            product.value = product_details.value
            updated = True
        response = ProductUpdateResponse(
            status = updated,
            data=self.product_to_response_model(product)
        )
        if updated:
            self.save_data()
        return response

    def remove_product(self, token, product_id):
        user = self.get_user_by_token(token)
        if not user:
            return False
        product_query = select(Product).where(
            and_(
                Product.user_id == user.id,
                Product.id == product_id
            )
        )
        try:
            product = self.session.execute(product_query).scalar_one()
            response = ProductDeletionResponse(
                data=self.product_to_response_model(product)
            )
        except sqlalchemy.exc.NoResultFound:
            return None
        self.session.delete(product)
        self.save_data()
        return response

    def save_data(self):
        self.session.commit()
        self.raw_db.backup(self.backup_db)
    
    def close_db(self):
        self.session.close()
        self.backup_db.close()
        self.raw_db.close()
