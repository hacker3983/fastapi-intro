# Task API

A simple REST API built with FastAPI for managing tasks.

## Features

* Create tasks
* View all tasks
* Get a task by ID
* Update task completion status
* Delete tasks
* Custom error handling
* Pydantic request and response models

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* Requests

## API Endpoints

### Create Task

POST `/tasks`

### Get All Tasks

GET `/tasks`

### Get Task By ID

GET `/tasks/{task_id}`

### Update Task Status

PUT `/tasks/{task_id}`

### Delete Task

DELETE `/tasks/{task_id}`

## Example Task

```json
{
    "name": "Bed Time",
    "description": "Go to bed at 8 pm"
}
```

## What I Practiced

* CRUD operations
* FastAPI routing
* Path parameters
* Query parameters
* Pydantic models
* Response models
* HTTP exceptions
* Automated API testing with Python Requests

```
```
