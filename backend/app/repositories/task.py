from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self):
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM:
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        self.db.flush()
        return new_task

    def delete(self, task: TaskORM) -> None:
        self.db.delete(task)


