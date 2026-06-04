📚 Library API (FastAPI)

A simple REST API built with FastAPI for managing a library system. Supports full CRUD operations, advanced filtering, and strict request validation using Pydantic v2.

🚀 Features
Create, update, delete books
Get book by ID
Filter books by:
author
title
year
availability
pages (exact, min, max)
Get available / unavailable books
Get latest book
Strong validation with Pydantic
Clean modular structure (requests / responses / errors)
Automatic API docs via FastAPI
🧠 Tech Stack
Python
FastAPI
Pydantic
Uvicorn
📦 API Endpoints
Books
POST /books → Create book
GET /books → Get all books (with filters)
GET /books/{id} → Get book by ID
PUT /books/{id} → Update book
DELETE /books/{id} → Delete book
Extras
GET /books/count
GET /books/latest
GET /books/available
GET /books/unavailable
🔍 Filtering Example
GET /books?author=Gerry%20Conway&min_pages=100&year=1973
📄 Validation

All requests are validated using Pydantic:

Title/author length limits
Year range (≤ current year)
Pages must be > 0
Strict update validation for partial updates
📁 Project Structure
models/
  requests.py
  responses.py
  errors.py
main.py
testapi-endpoints.py
⚡ Run Project
uvicorn main:app --reload

Then open:

http://127.0.0.1:8000/docs
🧪 Testing

Run:

python testapi-endpoints.py
