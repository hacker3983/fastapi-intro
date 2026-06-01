from pydantic import BaseModel

class TaskAPIStatus(BaseModel):
    name: str = "Task API"
    status: str = "Online!"
    version: float = 0.1

class TaskModel(BaseModel):
    name: str
    description: str

class TaskCreation(BaseModel):
    id: int
    name: str
    description: str
    status: bool = False

class TaskCreationUpdateResponse(BaseModel):
    message: str
    data: TaskCreation
