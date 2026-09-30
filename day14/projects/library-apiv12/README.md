# Library API — Day 14
SQLAlchemy Transactions, Commit/Rollback & Service-Layer Architecture

This project is the Day 14 iteration of my FastAPI Library API.

The main focus of this day was learning how SQLAlchemy transactions work in a real backend application and refactoring the API so that transaction boundaries are controlled by the service layer.

The project now separates database operations from transaction coordination:

The database layer performs queries and database mutations.
The service layer coordinates business operations and transaction boundaries.
Services commit successful write operations.
Services roll back transactions when an expected operation failure requires it.
Database backups occur only after a successful commit.
What I Learned
Database Sessions

A SQLAlchemy Session is a short-lived object used by an application to interact with the database and manage ORM state and transactions.

The application creates a session for each request through a FastAPI dependency rather than maintaining one persistent session inside the database class.

Transactions

A transaction groups database changes into a logical unit of work.

A successful transaction is finalized with:

session.commit()

If a transaction needs to be undone before it is committed:

session.rollback()

Rollback only affects changes that are part of the current uncommitted transaction. It cannot undo changes that were committed previously.

flush() vs commit()

The database layer can use:

session.flush()

when SQLAlchemy needs to send pending changes to the database before the transaction is committed.

For example, add_book() flushes the newly created book so that generated database values such as the book ID are available before the service commits the transaction.

flush() does not finalize the transaction.

The service layer remains responsible for:

session.commit()
Service Layer

The service layer coordinates complete application operations.

For write operations, the service generally follows this pattern:

Service receives request
        ↓
Database layer performs operation
        ↓
Database changes remain uncommitted
        ↓
Service validates the result
        ↓
session.commit()
        ↓
Database backup
        ↓
Response returned

This keeps transaction boundaries aligned with logical business operations.

Architecture

The current request flow is:

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
Transaction
  ↓
SQLite Database
Routers

The routers/ package contains the API endpoints.

Routers primarily handle:

HTTP endpoints
Request parameters
Request models
Authentication dependencies
Response models
Passing requests to the appropriate service

Routers do not directly coordinate database transactions.

Services

The services/ package contains application-level operations:

services/
├── auth.py
├── users.py
└── books.py

Services are responsible for coordinating logical operations and transaction boundaries.

For successful write operations, services call:

session.commit()

When an expected business failure requires the current transaction to be abandoned, services call:

session.rollback()
Database Layer

library_db.py contains the SQLAlchemy engine and database operations.

The LibraryDB class is responsible for:

Database initialization
SQLite database creation
SQLAlchemy queries
Creating and modifying records
Soft deletion
Book restoration
Database backups

The database layer does not own the transaction boundary and does not commit successful service operations.

Database methods perform the required database work and leave transaction coordination to the service layer.

Transaction Architecture

The application uses the service layer as the transaction boundary.

Successful write operation

For example, creating a book follows this pattern:

Router
  ↓
Service
  ↓
LibraryDB.add_book()
  ↓
session.add()
  ↓
session.flush()
  ↓
Return result
  ↓
Service calls session.commit()
  ↓
Service calls backup()

The database operation itself does not commit.

Rollback on expected failure

If an operation fails in a way that leaves the current transaction needing to be abandoned, the service rolls back:

session.rollback()

The application then stops the operation rather than committing partial changes.

Atomic book imports

Book imports are treated as one logical transaction.

The service processes each book using the same session:

Book 1
  ↓
flush

Book 2
  ↓
flush

Book 3
  ↓
flush

All successful
  ↓
ONE commit

If an expected failure occurs during the import:

Book 1
  ↓
flush

Book 2
  ↓
flush

Book 3 fails
  ↓
rollback
  ↓
stop import

This prevents a partially completed import from being committed.

Commit and Backup

Database commits and backups are deliberately separate operations.

The normal successful write flow is:

Database changes
      ↓
session.commit()
      ↓
Database state is finalized
      ↓
my_library.backup()

The backup occurs after the commit.

This is important because a backup failure cannot undo a database transaction that has already been committed.

Rollback therefore applies to the database transaction before commit, not to external work performed afterward.

Exception Handling

Not every exception requires a transaction rollback.

Authentication failures

InvalidTokenError represents an authentication failure.

It is handled separately by the service layer and does not inherently require a rollback because authentication can fail before any database changes have been made.

Business-operation failures

Expected operation failures can require a rollback when changes have already been made during the current transaction.

For example, an unsuccessful book import can roll back the current transaction before returning the appropriate API error.

Database errors

Database/SQLAlchemy errors require deliberate transaction handling because a failed database operation can leave the SQLAlchemy session in a failed transaction state.

Unexpected database-error handling is tested separately from normal business-error handling.

The application does not use a blanket except Exception as a substitute for understanding which errors require rollback.

Important Architectural Decisions
1. Services own transaction boundaries

Transaction boundaries belong in the service layer because a service represents a logical application operation.

This allows an operation involving multiple database calls to be committed as one unit.

2. The database layer does not commit

LibraryDB performs database operations but does not decide when the overall business operation is complete.

This prevents individual database methods from committing changes prematurely.

3. flush() is used when generated values are needed

add_book() uses session.flush() so that generated values such as the new book ID can be available before the transaction is committed.

The transaction remains active after flush().

4. Imports use one transaction

A book import is treated as one logical operation.

The entire batch is committed once after every book succeeds.

If the operation fails before the commit, the transaction can be rolled back so that the import does not leave partially committed data.

5. Backups happen after commits

The database must be successfully committed before the backup is created.

A backup failure after a successful commit is a separate failure from the database transaction itself and cannot be undone with session.rollback().

6. Authentication errors are separate from transaction failures

An invalid JWT is an authentication problem, not automatically a database transaction problem.

InvalidTokenError therefore remains separately handled rather than being treated as a reason to blindly roll back every request.

7. No shared request session

Each request receives its own SQLAlchemy session through the FastAPI dependency.

The global LibraryDB instance contains the database engine and infrastructure, not a shared request session.

Database Session Lifecycle

A typical request follows this lifecycle:

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
Service commits or rolls back when required
      ↓
Request finishes
      ↓
Session context exits
      ↓
Session is closed

The active request session is not stored globally.

The application does have a global LibraryDB instance, but it contains the database engine rather than a shared request session.

Authentication

The API uses:

OAuth2 password flow
JWT access tokens
Argon2 password hashing
Role-based authorization

Supported roles:

user
admin
librarian

Access tokens are used to authenticate protected endpoints.

Features

The API currently supports:

User registration
User authentication
JWT access tokens
Role management
Role-based authorization
User lookup
Book creation
Book retrieval
Book updates
Soft deletion
Book restoration
Book statistics
Book counts
Available/unavailable filtering
Searching and filtering
Sorting
Pagination
Book importing
Book exporting
Ownership-based access
Database backups
Testing

The project contains dedicated test scripts covering the API's major functionality.

Testing includes:

API status
User registration
Authentication
Multiple user roles
Authorization
Invalid tokens
Missing tokens
Book CRUD operations
Soft deletion
Book restoration
Book imports
Book exports
Filtering
Sorting
Pagination
Book statistics
Ownership behavior
Transaction behavior
Import atomicity

The transaction refactor was regression-tested after the architectural changes.

The tests confirmed that:

Book creation still works.
Book updates still work.
Book deletion still works.
Book restoration still works.
Successful imports commit correctly.
Invalid import requests are rejected before database changes are committed.
Existing API behavior remains functional after moving transaction boundaries into the service layer.
Project Structure
library-apiv12/
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
Day 14 Main Takeaway

The main goal of Day 14 was to understand and correctly apply SQLAlchemy transactions in a layered FastAPI application.

The project now follows the pattern:

HTTP Request
     ↓
Router
     ↓
Service
     ↓
Database Operation
     ↓
SQLAlchemy Session
     ↓
Transaction
     ↓
Commit / Rollback
     ↓
Database

The key architectural principle is:

The database layer performs database operations. The service layer decides when the logical operation should be committed or rolled back.

This creates clear transaction boundaries and allows multiple database operations to participate in one logical business transaction.

Day 14 also reinforced that:

flush() is not the same as commit().
rollback() only undoes uncommitted transaction changes.
A later rollback cannot undo an earlier commit.
A failed database operation can leave a session requiring rollback before it can continue.
Transaction boundaries should match logical business operations.
Post-commit operations such as backups are separate from the database transaction itself.
