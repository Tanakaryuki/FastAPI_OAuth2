from fastapi import FastAPI

from api.routers import user,task

app = FastAPI()
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(task.router, prefix="/api", tags=["tasks"])