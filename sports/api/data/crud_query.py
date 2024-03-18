"""SQLAlchemy Query Functions"""
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

import models

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()


def get_performances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Performance
                    ).offset(skip).limit(limit).all()

def get_leagues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.League
                    ).options(joinedload(models.League.teams)
                              ).offset(skip).limit(limit).all()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team
                    ).offset(skip).limit(limit).all()