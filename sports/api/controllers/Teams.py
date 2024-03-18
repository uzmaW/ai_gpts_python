
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from data import crud_query as crud, schemas
from database import get_db


t_router = APIRouter()

@t_router.get("/v0/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams