from fastapi import FastAPI

from api.routers import user,task

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
app.include_router(user.router, prefix="/api")
app.include_router(task.router, prefix="/api")