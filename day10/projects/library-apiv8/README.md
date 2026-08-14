# Library API v8

A FastAPI library management API built while learning backend development with Python.

## Features

- User registration and authentication
- JWT access tokens
- Password hashing
- User-owned books
- Create, read, update and soft-delete books
- Filtering and sorting
- Pagination
- Book statistics
- Available/unavailable book filtering
- SQLite database
- SQLAlchemy ORM
- Alembic database migrations
- Database backups and recovery

## Soft Delete

Books aren't permanently removed from the database when deleted.

Instead, the `deleted_at` column is populated with the deletion timestamp. Normal queries exclude books where `deleted_at` is set.

This allows deleted records to remain available for recovery or auditing.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT
- Pydantic

## Running the API

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
