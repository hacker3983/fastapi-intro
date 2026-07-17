import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import *

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

    def add_product(self, product_details: ProductCreationRequest):
        new_product = Product(
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

    def get_products(self):
        query = select(Product)
        results = self.session.execute(query).all()
        responses = self.query_results_to_response_models(results)
        return responses

    def get_product(self, product_id):
        product = self.session.get(Product, product_id)
        if product:
            response = self.product_to_response_model(product)
        else:
            response = None
        return response

    def update_product(self, product_id, product_details: ProductUpdateRequest):
        product = self.session.get(Product, product_id)
        updated = False
        if not product:
            return None
        if product_details.name:
            product.name = product_details.name
            updated = True
        if product_details.description:
            product.description = product_details.description
            updated = True
        if product_details.value is not None:
            product.value = product_details.value
            updated = True
        response = None
        if updated:
            response = ProductUpdateResponse(
                data=self.product_to_response_model(product)
            )
            self.save_data()
        return response

    def remove_product(self, product_id):
        product = self.session.get(Product, product_id)
        if not product:
            return None
        response = ProductDeletionResponse(
            data=self.product_to_response_model(product)
        )
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
