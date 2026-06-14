# Library API (FastAPI V3)

A RESTful Library Management API built with FastAPI.

This project demonstrates CRUD operations, filtering, sorting, pagination, validation, and API documentation using FastAPI and Pydantic.

## Features

### Core Features

* Create books
* Retrieve all books
* Retrieve a book by ID
* Update books
* Delete books

### Search & Filtering

* Filter by author
* Filter by title
* Filter by publication year
* Filter by availability
* Filter by exact page count
* Filter by minimum pages
* Filter by maximum pages

### Sorting

* Sort by title
* Sort by year
* Sort by pages
* Ascending order (default)
* Descending order

### Pagination

* Limit number of results
* Offset support

### Statistics

* Total books
* Available books
* Unavailable books

### Additional Endpoints

* Book count endpoint
* Latest book endpoint
* Available books endpoint
* Unavailable books endpoint

### Validation

* Pydantic request models
* Input validation
* Custom error handling
* Automatic OpenAPI documentation

## Technologies Used

* Python
* FastAPI
* Pydantic

## API Endpoints

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| GET    | /                  | API status         |
| POST   | /books             | Create book        |
| GET    | /books             | Get books          |
| GET    | /books/{id}        | Get book by ID     |
| PUT    | /books/{id}        | Update book        |
| DELETE | /books/{id}        | Delete book        |
| GET    | /books/count       | Total books        |
| GET    | /books/latest      | Latest book        |
| GET    | /books/available   | Available books    |
| GET    | /books/unavailable | Unavailable books  |
| GET    | /books/stats       | Library statistics |

## Example Pagination

GET /books?limit=5

GET /books?limit=5&offset=10

## Example Sorting

GET /books?sort_by=title

GET /books?sort_by=year&order=desc

GET /books?sort_by=pages

## Future Improvements

* JSON persistence
* SQLite integration
* SQLAlchemy ORM
* Authentication
* Deployment
