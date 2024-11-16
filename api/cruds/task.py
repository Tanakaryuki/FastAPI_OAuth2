from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.task as task_schema


def create_task(
    db: Session, task: task_schema.TaskCreateRequest
) -> task_model.Task | None:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def read_task_by_id(db: Session, id: str, username: str) -> task_model.Task | None:
    return (
        db.query(task_model.Task)
        .filter(
            task_model.Task.id == id, task_model.Task.administrator_username == username
        )
        .first()
    )
