from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)
class TaskSchema(BaseModel):
    id : str
    title : str
    completed : bool

class TasksCreateSchema(BaseModel):
    title:str

class TaskUpdateSchema(BaseModel):
    title:str | None=None
    completed:bool | None=None


tasks: list[TaskSchema] = []

# @app.get("/")
# def read_base_page():
#     return {"message": "hello world"}{}


@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks")
def create_task(payload: TasksCreateSchema)-> TaskSchema:
    new_tasks = TaskSchema(id=str(uuid4()), title=payload.title,completed=False)

    tasks.append(new_tasks)
    return new_tasks

@app.patch("/tasks/{tasks_id}")
def update_task(tasks_id:str, payload:TaskUpdateSchema):
    for task in tasks:
        if task.id == tasks_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
               task.completed = payload.completed
            return task
        
@app.delete("/tasks/{tasks_id}")
def delete_task(tasks_id: str):
    for task in tasks:
        if task.id == tasks_id:
            tasks.remove(task)
            return {"message": "deleted"}
        