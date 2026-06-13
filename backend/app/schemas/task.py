from pydantic import BaseModel

class TaskSchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    title: str
    completed: bool

class CategorySchema(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str


class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

