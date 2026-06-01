from fastapi import FastAPI, HTTPException
from models import *

tasks = []
task_id_counter = 0

app = FastAPI()

def create_new_task(task_details: TaskModel):
    global task_id_counter
    task_id_counter += 1
    new_task = {
            "id": task_id_counter,
            "name": task_details.name,
            "description": task_details.description,
            "status": False
    }
    return new_task

def find_task_by_id(task_id):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            return (i, task)
    return None

def task_not_found_error():
    raise HTTPException(
        status_code=404,
        detail="The requested task or resource was not found!"
    )

@app.get("/")
def home():
    return TaskAPIStatus()

@app.post("/tasks")
def add_task(task_details: TaskModel):
    task = create_new_task(task_details)
    tasks.append(task)
    response = TaskCreationUpdateResponse(
        message="Task created",
        data=TaskCreation.model_validate(task)
    )
    return response

@app.get("/tasks")
def get_tasks():
    return {"Tasks": tasks}

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    result = find_task_by_id(task_id)
    if not result:
        task_not_found_error()
    task = result[1]
    return task

@app.put("/tasks/{task_id}")
def mark_task_status_by_id(task_id: int, status: bool):
    result = find_task_by_id(task_id)
    if not result:
        task_not_found_error()
    task = result[1]
    print(status, type(status))
    task["status"] = status
    response = TaskCreationUpdateResponse(
        message="Task updated",
        data=TaskCreation.model_validate(task)
    )
    return response

@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int):
    result = find_task_by_id(task_id)
    if not result:
        task_not_found_error()
    task_index = result[0]
    task = result[1]
    response = TaskCreationUpdateResponse(
        message="Task deleted",
        data=TaskCreation.model_validate(task)
    )
    tasks.pop(task_index)
    return response
