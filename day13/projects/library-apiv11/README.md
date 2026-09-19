# Library API — Day 13

## Database Sessions, Dependencies & Service-Layer Architecture

This project is the Day 13 iteration of my FastAPI Library API.

The main focus of this day was learning how to properly manage SQLAlchemy database sessions with FastAPI dependencies and introducing a service layer to separate API routing from application logic.

---

## What I Learned

### Database Sessions

A SQLAlchemy `Session` is a short-lived object used by an application to interact with the database and manage ORM state and transactions.

Instead of maintaining one persistent session inside the database class, the application now creates a session for each request.

### FastAPI Dependencies

FastAPI's dependency injection system is used to provide database sessions to endpoints.

The database session dependency uses `yield` so the session can be provided to the request and then closed automatically when the dependency finishes.

### Service Layer

Business/application operations were moved out of the routers and into dedicated service modules.

The routers are now primarily responsible for handling HTTP/API concerns while services coordinate application operations.

---

## Architecture

The current request flow is:

```text
Client
  ↓
FastAPI
  ↓
Router
  ↓
Service Layer
  ↓
LibraryDB
  ↓
SQLAlchemy Session
  ↓
SQLite Database
```

### Routers

The `routers/` package contains the API endpoints:

```text
routers/
├── __init__.py
├── auth.py
├── users.py
└── books.py
```

Routers handle:

* HTTP endpoints
* Request parameters
* Request models
* Authentication dependencies
* Response models
* Passing requests to the appropriate service

### Services

The `services/` package contains application-level operations:

```text
services/
├── auth.py
├── users.py
└── books.py
```

Services receive the database session and coordinate operations with `LibraryDB`.

### Database Layer

`library_db.py` contains the SQLAlchemy engine and database operations.

The `LibraryDB` class is responsible for:

* Database initialization
* SQLite database creation
* SQLAlchemy queries
* Creating and modifying records
* Soft deletion
* Book restoration
* Database commits
* Database backups

### Dependencies

`dependencies.py` contains FastAPI dependencies.

The database session is created per request:

```python
def get_db():
    with Session(my_library.db) as session:
        yield session
```

The session is then injected into endpoints through:

```python
db_session = Annotated[Session, Depends(get_db)]
```

---

## Database Session Lifecycle

A typical request follows this lifecycle:

```text
Request arrives
      ↓
FastAPI resolves get_db()
      ↓
SQLAlchemy Session is created
      ↓
Session is provided to the endpoint
      ↓
Router calls the service
      ↓
Service calls LibraryDB
      ↓
Database operations are performed
      ↓
Changes are committed when required
      ↓
Request finishes
      ↓
Session context exits
      ↓
Session is closed
```

The active request session is **not stored globally**.

The application does have a global `LibraryDB` instance, but it contains the database engine rather than a shared request session.

---

## Authentication

The API uses:

* OAuth2 password flow
* JWT access tokens
* Argon2 password hashing
* Role-based authorization

Supported roles:

```text
user
admin
librarian
```

Access tokens are used to authenticate protected endpoints.

---

## Features

The API currently supports:

* User registration
* User authentication
* JWT access tokens
* Role management
* Role-based authorization
* User lookup
* Book creation
* Book retrieval
* Book updates
* Soft deletion
* Book restoration
* Book statistics
* Book counts
* Available/unavailable filtering
* Searching and filtering
* Sorting
* Pagination
* Book importing
* Book exporting
* Ownership-based access
* Database backups

---

## Testing

A dedicated test script is included:

```text
test-scripts/
└── testapi-endpoints.py
```

The script tests functionality including:

* API status
* User registration
* Authentication
* Multiple user roles
* Authorization
* Invalid tokens
* Missing tokens
* Book CRUD operations
* Soft deletion
* Book restoration
* Book imports
* Book exports
* Filtering
* Sorting
* Pagination
* Book statistics
* Ownership behavior

The database was also inspected after testing to verify that operations were actually persisted.

---

## Project Structure

```text
library-apiv13/
├── main.py
├── library_db.py
├── dependencies.py
├── helpers.py
├── models/
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── books.py
├── services/
│   ├── auth.py
│   ├── users.py
│   └── books.py
├── migrations/
├── test-scripts/
├── alembic.ini
├── requirements.txt
├── library.db
└── backups.db
```

---

## Day 13 Architecture Notes

This iteration introduces a cleaner separation between the API layer and application operations.

The routers no longer directly perform database operations. Instead, they pass the request information and database session to the appropriate service.

The service layer then coordinates the operation with the database layer.

There are still areas that can be improved in future iterations, particularly the separation between business logic, database operations, HTTP-specific errors, and API response models.

These are intentional areas for future architectural refinement rather than requirements for this iteration.

---

## Main Takeaway

The main goal of Day 13 was to understand how database sessions, FastAPI dependencies, and service-layer architecture work together.

The project now follows the general pattern:

```text
HTTP Request
     ↓
Router
     ↓
Service
     ↓
Database Layer
     ↓
SQLAlchemy Session
     ↓
Database
```

This provides a foundation for building larger and more maintainable backend applications.
