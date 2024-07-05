from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import api.schemas.task as task_schema
import api.cruds.task as task_crud
import api.models.user as user_model
from api.utils.auth import get_current_user
from api.db import get_db

router = APIRouter()

@router.post("/task", description="新しいタスクを作成するために使用されます。")
def create_event(request: task_schema.TaskCreateRequest,current_user: user_model.User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = task_crud.create_task(db=db,administrator_username=current_user.username,task=request)
    if not event:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED

@router.get("/task/{id}", response_model=task_schema.TaskDeteilResponse, description="タスク詳細を取得するために使用されます。")
def get_task(id: str,current_user: user_model.User = Depends(get_current_user),db: Session = Depends(get_db)):
    task = task_crud.read_task_by_id(db=db,id=id,username=current_user.username)
    return task