
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from data import crud_query as crud, schemas
from database import get_db


pr_router = APIRouter()

pr_router.get("/v0/performances/", response_model=list[schemas.Performance])
def read_performances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    performances = crud.get_performances(db, skip=skip, limit=limit)
    return performances

pr_router.get("/v0/leagues/", response_model=list[schemas.League])
def read_leagues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leagues = crud.get_leagues(db, skip=skip, limit=limit)
    return leagues
