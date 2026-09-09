# Library API v10

A RESTful library management API built with **Python and FastAPI**.

This project started as a single-file FastAPI application and was later refactored into a modular architecture using routers, dependencies, helper modules, models, and database logic.

The main goal of v10 was to improve the application's **architecture, maintainability, and separation of concerns without breaking existing functionality**.

## 🚀 Features

* User signup and authentication
* JWT-based authentication
* Role-based authorization
* Admin and librarian permissions
* User management
* Book CRUD operations
* Book ownership
* Book searching and filtering
* Pagination
* Sorting
* Available/unavailable book filtering
* Book statistics
* Book import/export
* Soft deletion
* Book restoration
* Input validation
* API documentation with Swagger UI
* Regression testing

## 🏗️ Project Structure

```text
library-apiv10/
├── main.py
├── library_db.py
├── dependencies.py
├── helpers.py
├── models/
│   ├── __init__.py
│   ├── database.py
│   ├── errors.py
│   ├── models.py
│   ├── requests.py
│   └── responses.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── books.py
├── migrations/
├── test-scripts/
├── alembic.ini
├── requirements.txt
└── library.db
```

## 🧩 Architecture

The application uses **separation of concerns** to keep different responsibilities in their own modules.

### `main.py`

Responsible primarily for:

* Creating the FastAPI application
* Registering routers
* Providing the API information endpoint

### `routers/`

Contains the API route definitions.

* `auth.py` — authentication and signup/signin
* `users.py` — user management and role modification
* `books.py` — book-related operations

### `dependencies.py`

Contains shared FastAPI dependencies and application-level dependencies such as the OAuth2 security scheme and database interface.

### `helpers.py`

Contains reusable error-handling functions used throughout the API.

### `models/`

Contains the application's database models, request models, response models, and related model definitions.

### `library_db.py`

Contains the main database/application logic used by the API.

## 🔐 Authentication & Authorization

The API uses OAuth2 bearer tokens with JWT authentication.

Users can have different roles, including:

* User
* Librarian
* Admin

Protected endpoints validate the user's access token and enforce the appropriate permissions.

The application also handles invalid and missing authentication tokens.

## 📚 API Routes

### Authentication

```text
POST /api/v10/signup
POST /api/v10/signin
```

### Users

```text
GET   /api/v10/users
GET   /api/v10/users/{user_id}
PATCH /api/v10/users/{user_id}/role
```

### Books

```text
POST   /api/v10/books
POST   /api/v10/books/{book_id}/restore

GET    /api/v10/books
GET    /api/v10/books/all
GET    /api/v10/books/count
GET    /api/v10/books/latest
GET    /api/v10/books/available
GET    /api/v10/books/unavailable
GET    /api/v10/books/stats
GET    /api/v10/books/export
GET    /api/v10/books/{book_id}

POST   /api/v10/books/import

PUT    /api/v10/books/{book_id}
DELETE /api/v10/books/{book_id}
```

## 🧪 Testing

The project includes manual integration test scripts using Python's `requests` library.

Testing covered:

* Authentication
* Authorization
* Invalid credentials
* Invalid tokens
* Missing tokens
* User permissions
* Admin permissions
* Librarian permissions
* Book ownership
* CRUD operations
* Soft deletion
* Restoration
* Searching/filtering
* Pagination
* Sorting
* Statistics
* Import/export
* Input validation
* Regression testing after the architectural refactor

The database was also reset and the application was tested again after the refactor to verify that existing functionality continued working.

## ▶️ Running the Project

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API documentation is available through FastAPI's automatically generated Swagger UI.

```text
http://localhost:8000/docs
```

## 🎯 What I Learned

This project taught me how to refactor a FastAPI application into a more maintainable architecture.

Key concepts learned:

* Separation of concerns
* Python modules
* Python packages
* `__init__.py`
* FastAPI `APIRouter`
* Router prefixes and tags
* Dependency organization
* Refactoring an existing application
* Regression testing
* Maintaining functionality while changing architecture
* Organizing a growing FastAPI project

## 📈 Project Progression

This version represents the transition from a large, centralized FastAPI application into a modular API architecture.

The focus of v10 was **not adding a large number of new features**, but improving how the existing application was organized and maintained.

## 🛠️ Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Alembic
* JWT
* OAuth2
* Pydantic
* Argon2
* Requests

---

**Library API v10 — Backend Engineering Learning Project**

