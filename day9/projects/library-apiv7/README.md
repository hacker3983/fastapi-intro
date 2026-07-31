# Library API v7

A production-style REST API built with FastAPI, SQLAlchemy, SQLite, and JWT authentication.

## Features

- User registration and authentication
- JWT token based authorization
- Argon2 password hashing
- User-owned book collections
- CRUD operations
- Pagination
- Sorting
- Import/export
- Database backup and restore
- Request validation with Pydantic

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- Argon2

## Installation

Clone repository:

```bash
git clone <repo-url>
cd library-apiv7
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

API available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## Authentication

Users can create accounts and receive JWT access tokens.

Passwords are securely stored using Argon2 hashing.

## Database Recovery

The API automatically restores the database from backup if the primary SQLite database is missing.

Example:

```bash
rm library.db
uvicorn main:app --reload
```

Output:

```
Successfully restored database from backup!
```

## Project Structure

```
library-apiv7/
│
├── main.py
├── library_db.py
├── models/
├── backups.db
├── library.db
└── testapi-endpoints.py
```

## Future Improvements

- Add Alembic migrations
- Add PostgreSQL support
- Add Docker deployment
- Add automated pytest suite
- Add CI/CD pipeline
