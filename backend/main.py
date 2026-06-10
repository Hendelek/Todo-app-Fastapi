from uuid import uuid4
from fastapi import FastAPI, HTTPException
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
        
class CategorySchema(BaseModel):
    id: str
    name: str
 
class CategoryCreateSchema(BaseModel):
    name: str
 
class CategoryUpdateSchema(BaseModel):
    name: str | None = None
 
 
categories: list[CategorySchema] = []
 
 
@app.get("/categories")
def read_categories() -> list[CategorySchema]:
    return categories
 
 
@app.post("/categories", status_code=201)
def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category
 
 
@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryUpdateSchema) -> CategorySchema:
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category
    raise HTTPException(status_code=404, detail="Category not found")
 
 
@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=404, detail="Category not found")