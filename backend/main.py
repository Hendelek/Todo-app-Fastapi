from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))



class TaskORM(Base):
    __tablename__="tasks"

    title:Mapped[str]

    completed :Mapped [bool] = mapped_column(default=False)
    

@asynccontextmanager
async def lifespan(_:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)

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

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:

     db.close()
    

# @app.get("/")
# def read_base_page():
#     return {"message": "hello world"}{}


@app.get("/tasks")
def read_tasks(db:Session = Depends(get_db)) -> list[TaskSchema]:
    return db.query(TaskORM).all()


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