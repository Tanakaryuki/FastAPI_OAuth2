from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

@router.post("/task", description="新しいタスクを作成するために使用されます。", tags=["tasks"])
def create_event(request: task_schema.TaskCreateRequest, db: Session = Depends(get_db)):
    event = task_crud.create_task(db=db,task=request)
    if not event:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED

@router.get("/task/{id}", response_model=task_schema.TaskDeteilResponse, description="タスク詳細を取得するために使用されます。", tags=["tasks"])
def get_task(id: str,db: Session = Depends(get_db)):
    task = task_crud.read_task_by_id(db=db,id=id)
    return task