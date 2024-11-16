from sqlalchemy.orm import Session

import api.cruds.task as task_crud
import api.schemas.task as task_schema
import api.models.task as task_model


def create_task(
    db: Session, administrator_username: str, task: task_schema.TaskCreateRequest
) -> None:
    if (
        task_crud.read_task_by_id(db=db, id=task.id, username=administrator_username)
        is not None
    ):
        raise ValueError("Task already exists")
    task = task_model.Task(
        administrator_username=administrator_username, **task.model_dump()
    )
    task_crud.create_task(db=db, task=task)
    return None

def get_task(db: Session, id: str, username: str) -> task_model.Task:
    task = task_crud.read_task_by_id(db=db, id=id, username=username)
    if task is None:
        raise ValueError("Task not found")
    return task
