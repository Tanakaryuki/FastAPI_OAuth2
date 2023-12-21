from sqlalchemy.orm import Session
from sqlalchemy import and_

import api.models.task as task_model
import api.schemas.task as task_schema

def create_task(db: Session, administrator_username: str, task: task_schema.TaskCreateRequest) -> task_model.Task | None:
    if read_task_by_id(db=db,id=task.id):
        return None
    task_dict = task.model_dump()
    task = task_model.Task(administrator_username=administrator_username,**task_dict)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def read_task_by_id(db: Session, id: str,username: str) -> task_model.Task | None:
    return db.query(task_model.Task).filter(and_(task_model.Task.id == id,task_model.Task.administrator_username == username)).first()