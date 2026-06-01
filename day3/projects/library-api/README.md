# Library API

A REST API built with FastAPI for managing a collection of books.

## Features

* Create books
* View all books
* Get books by ID
* Update book information
* Delete books
* Search books by author
* Search books by title
* Search books by publication year
* Combine multiple search filters
* Get latest published book
* Get total book count
* Input validation using Pydantic
* Response models
* Custom error handling

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* Requests

## API Endpoints

### Create Book

POST `/books`

### Get All Books

GET `/books`

### Search Books

GET `/books?author=AUTHOR`

GET `/books?title=TITLE`

GET `/books?year=YEAR`

GET `/books?author=AUTHOR&year=YEAR`

### Get Book By ID

GET `/books/{book_id}`

### Update Book

PUT `/books/{book_id}`

### Delete Book

DELETE `/books/{book_id}`

### Get Latest Book

GET `/books/latest`

### Get Book Count

GET `/books/count`

## Example Book

```json
{
    "title": "Maximum Carnage",
    "author": "Tom DeFalco",
    "year": 1994,
    "pages": 150,
    "available": false
}
```

## Validation Rules

* Title cannot be empty
* Author cannot be empty
* Year must be greater than 0
* Pages must be greater than 0

## What I Practiced

* CRUD operations
* Query parameter filtering
* Combining search filters
* Response models
* Pydantic validation
* HTTP exceptions
* FastAPI routing
* Automated endpoint testing
* Data modeling with Pydantic

```
```
