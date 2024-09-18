from fastapi import FastAPI
import uvicorn
import logging

from .settings import Settings as settings
from .controllers.routers import  routes_list
from .database import setup_database
#from fastapi.middleware.cors import CORSMiddleware
from .data.schemas import TaskBase, TaskOut, TodoOut, TodoBase
from .data.models import Task, Todo
from typing import Any
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
app: FastAPI = FastAPI()

app.title = settings.APP_NAME
app.description = settings.APP_DESCRIPTION
app.version = settings.APP_VERSION
app.debug = bool(settings.DEBUG)
#app.docs_url = settings.DOCS_URL
from fastapi import FastAPI, Request

app = FastAPI()
setup_database()

@app.middleware("http")
def check_http_https_middleware(request: Request, call_next):
    logger.info(f"app request: {request.url}")
    response = call_next(request)
    return response

from .database import get_db

for router in routes_list:
    app.include_router(router)

@app.get("/")
def index():
    return {"message": "FastAPI : Todo App"}

@app.post("/test", response_model=TodoOut)
def create_task(task_create:TodoBase, db:Session=Depends(get_db))->Any: 
        db_item = Todo(**task_create.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


"""_auto run server from code_"""
#if __name__ == "__main__":
#    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)