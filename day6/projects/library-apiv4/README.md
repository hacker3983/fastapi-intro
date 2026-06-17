# Day 6 – Library API v4

## Overview

This version expands the Library API into a much more feature-rich REST API built with FastAPI. The project now supports advanced searching, sorting, pagination, statistics, importing/exporting books, persistent storage, and automatic backup restoration.

## Features

* Create new books
* Retrieve all books
* Retrieve a book by ID
* Update existing books
* Delete books
* Search books by:

  * Title
  * Author
  * Year
  * Availability
  * Exact page count
  * Minimum pages
  * Maximum pages
* Sort books by:

  * Title
  * Year
  * Pages
* Ascending and descending sorting
* Pagination using `limit` and `offset`
* Get total book count
* Retrieve the latest book
* Retrieve available books
* Retrieve unavailable books
* Library statistics endpoint
* Export all books
* Import multiple books
* Persistent JSON storage
* Automatic backup restoration if the primary data file is missing
* Request validation using Pydantic models
* Structured response models
* Custom error handling
* Extensive endpoint testing with a dedicated test script

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn

## Example Endpoints

* `GET /books`
* `POST /books`
* `GET /books/{book_id}`
* `PUT /books/{book_id}`
* `DELETE /books/{book_id}`
* `GET /books/count`
* `GET /books/latest`
* `GET /books/available`
* `GET /books/unavailable`
* `GET /books/stats`
* `GET /books/export`
* `POST /books/import`

## Validation

The API validates incoming data automatically, including:

* Required fields
* String length limits
* Positive page counts
* Valid publication years
* Query parameter constraints for pagination

## Learning Objectives

* Building larger REST APIs with FastAPI
* Using request and response models
* Implementing filtering and pagination
* Data persistence with JSON files
* Backup and recovery mechanisms
* API validation and error handling
* Automated endpoint testing

