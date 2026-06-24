# 📚 Library API v5 (SQLite Edition)

A RESTful Library Management API built with **FastAPI** and **SQLite**. This version migrates the project from in-memory/JSON storage to a persistent SQLite database while keeping the existing API features and adding automatic backup and restoration support.

## ✨ Features

* Create, read, update, and delete books (CRUD)
* Search books by:

  * Author
  * Title
  * Year
  * Availability
  * Exact page count
  * Minimum pages
  * Maximum pages
* Sort results by:

  * Title
  * Year
  * Pages
* Ascending and descending ordering
* Pagination with `limit` and `offset`
* Book statistics
* Available and unavailable book endpoints
* Export books
* Import books
* SQLite database persistence
* Automatic backup database synchronization
* Automatic restoration from backup if the main database is missing
* Request validation using Pydantic models

## 🛠️ Tech Stack

* Python
* FastAPI
* SQLite (`sqlite3`)
* Uvicorn
* Pydantic

## 🚀 Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## 💾 Database

The project stores data in `library.db`.

A secondary backup database (`backups.db`) is automatically updated whenever changes are committed. If `library.db` is missing but `backups.db` exists, the application automatically restores the main database from the backup during startup.

## 🧪 Testing

The project includes test scripts for validating API functionality and database behavior:

* `testapi-endpoints.py`
* `test_database.py`

These tests cover CRUD operations, filtering, sorting, pagination, validation, statistics, import/export, and backup restoration.

## 📈 Version Highlights

Version 5 introduces:

* Migration from previous storage methods to SQLite
* Automatic database backups
* Automatic database restoration
* Improved persistence and reliability while preserving existing API functionality
