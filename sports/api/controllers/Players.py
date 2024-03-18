
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from data import crud_query as crud, schemas
from database import get_db

p_router = APIRouter()


@p_router.get("/v0/players/", response_model=list[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players


@p_router.get("/v0/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player