"""Database configuration - Schemas"""
from pydantic import BaseModel
from typing import List

class Performance(BaseModel):
    performance_id : int
    player_id : int
    week_number : str
    fantasy_points : float

    class Config:
        from_attributes = True


class PlayerBase(BaseModel):
    player_id : int
    first_name : str
    last_name : str

    class Config:
        from_attributes = True

class Player(PlayerBase):
    performances: List[Performance] = []

    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    league_id : int
    team_id : int
    team_name : str

    class Config:
        from_attributes = True

class Team(TeamBase):
    players: List[PlayerBase] = []

    class Config:
        from_attributes = True

class League(BaseModel):
    league_id : int
    league_name : str
    scoring_type : str
    teams: List[TeamBase] = []

    class Config:
        from_attributes = True