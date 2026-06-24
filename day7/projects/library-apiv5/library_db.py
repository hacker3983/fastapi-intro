import os
import sqlite3
from models.models import *

class LibraryDB:
    def __init__(self, file="library.db", backup_file="backups.db"):
        self.initialize_databases(file, backup_file)

    def initialize_databases(self, file, backup_file):
        if not os.path.isfile(file) and os.path.isfile(backup_file):
            self.create_database(file)
            self.create_backup_database(backup_file)
            self.restore_backup()
            print("Successfully restored database from backups!")
            return
        self.create_database(file)
        self.create_backup_database(backup_file)
        print("Successfully created / connected to the database!")

    def create_database(self, file):
        self.db = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_backup_database(self, backup_file):
        self.backup_db = sqlite3.connect(backup_file, check_same_thread=False)

    def restore_backup(self):
        self.backup_db.backup(self.db)

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title, author, year, pages, available)")

    def filter_books(self, author=None, title=None, year=None,
        available=None, pages=None, min_pages=None, max_pages=None,
        sort_by=None, order=None, limit=0, offset=0):
        arguments = []
        query = "SELECT * FROM books WHERE 1=1"
        if author:
            query += f" AND author LIKE ?"
            arguments.append(f"%{author}%")

        if title:
            query += f" AND title LIKE ?"
            arguments.append(f"%{title}%")

        if year:
            query += f" AND year = ?"
            arguments.append(year)

        if available is not None:
            query += f" AND available = {available}"

        if pages:
            query += f" AND pages = {pages}"

        if min_pages:
            query += f" AND pages >= {min_pages}"

        if max_pages:
            query += f" AND pages <= {max_pages}"
        
        sort_order = "ASC"
        if order and order.lower() == "desc":
            sort_order = "DESC"

        if sort_by == "title":
            query += f" ORDER BY title {sort_order}"
        elif sort_by == "pages":
            query += f" ORDER BY pages {sort_order}"
        elif sort_by == "year":
            query += f" ORDER BY year {sort_order}"
        
        if limit and limit > 0:
            query += " LIMIT ? OFFSET ?"
            arguments.extend([limit, offset])

        results = self.cursor.execute(query, arguments).fetchall()
        results = self.query_results_to_book_responses(results)
        return results 

    def get_books(self):
        results = self.cursor.execute("SELECT * FROM books").fetchall()
        results = self.query_results_to_book_responses(results)
        return results

    def get_book_by_id(self, book_id):
        result = self.cursor.execute("SELECT * FROM books where id = ?", (book_id,)).fetchone()
        result = self.query_result_to_book_response(result)
        return result

    def query_result_to_book_response(self, query_result):
        if not query_result:
            return None
        book_response = BookResponse(
                id=query_result[0],
                title=query_result[1],
                author=query_result[2],
                year=query_result[3],
                pages=query_result[4],
                available=query_result[5]
        )
        return book_response
    
    def query_results_to_book_responses(self, query_results):
        book_responses = [self.query_result_to_book_response(query_result) for query_result in query_results]
        return book_responses

    def get_book_count(self):
        books = self.get_books()
        if not books:
            return 0
        return len(books)

    def get_book_stats(self):
        result = self.cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(CASE WHEN available = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN available = 0 THEN 1 ELSE 0 END)
                FROM books
                """
        ).fetchone()
        if not result or result[0] == 0:
            return {
                "total_books": 0,
                "available_books": 0,
                "unavailable_books": 0,
            }
        return {
            "total_books": result[0],
            "available_books": int(result[1] or 0),
            "unavailable_books": int(result[2] or 0),
        }

    def get_latest_book(self):
        result = self.cursor.execute("SELECT * FROM books ORDER BY year DESC LIMIT 1").fetchone()
        if result:
            result = self.query_result_to_book_response(result)
        return result
    
    def get_available_books(self):
        available_books = self.filter_books(available=True)
        return available_books

    def get_unavailable_books(self):
        unavailable_books = self.filter_books(available=False)
        return unavailable_books

    def add_book(self, book_details: BookCreateRequest):
        result = self.cursor.execute(
            """INSERT INTO books
                (title, author, year, pages, available)
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                book_details.title, book_details.author,
                book_details.year, book_details.pages,
                True
            )
        )
        last_row_id = result.lastrowid
        book_response = self.get_book_by_id(last_row_id)
        self.save_data()
        return book_response

    def remove_book(self, book_id):
        book = self.get_book_by_id(book_id)
        result = self.cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )
        self.save_data()
        return book

    def update_book(self, book_id, book_details: BookUpdateRequest):
        updated = False
        if book_details.title:
            self.cursor.execute("UPDATE books SET title = ? WHERE id = ?", (book_details.title, book_id))
            updated = True

        if book_details.author:
            self.cursor.execute("UPDATE books SET author = ? WHERE id = ?", (book_details.author, book_id))
            updated = True

        if book_details.year:
            self.cursor.execute("UPDATE books SET year = ? WHERE id = ?", (book_details.year, book_id))
            updated = True

        if book_details.pages:
            self.cursor.execute("UPDATE books SET pages = ? WHERE id = ?", (book_details.pages, book_id))
            updated = True

        if book_details.available is not None:
            self.cursor.execute("UPDATE books SET available = ? WHERE id = ?", (book_details.available, book_id))
            updated = True
        if updated:
            self.save_data()
        return self.get_book_by_id(book_id)

    def save_data(self):
        self.db.commit()
        self.db.backup(self.backup_db)

    def close_db(self):
        self.backup_db.close()
        self.db.close()
