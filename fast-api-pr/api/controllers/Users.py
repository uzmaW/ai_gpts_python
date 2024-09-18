
from turtle import update
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List 
from ..repositories.UserRepository import UserRepository
from ..data.schemas import User,UserBasic,UserCreate,UserOut,UserUpdate
from ..database import get_db


class Users:
        
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["user"])
        self.router.add_api_route("/"    , self.get_users,   methods=["GET"],    response_model=List[UserOut])
        self.router.add_api_route("/"    , self.create_user, methods=["POST"],   response_model=UserOut)
        self.router.add_api_route("/{id}", self.get_user,    methods=["GET"],    response_model=UserOut)
        self.router.add_api_route("/{id}", self.update_user, methods=["PUT"],    response_model=UserOut)
        self.router.add_api_route("/{id}", self.delete_user, methods=["DELETE"], response_model=UserOut)

    @staticmethod
    def get_by_name(username: str, db:Session=Depends(get_db)) -> UserOut:
        return UserRepository(db).get_by_name(username) 

    def get_user(self, id:int,  db:Session=Depends(get_db)) -> User:
        user = UserRepository(db).get_by_id(id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
        
    
    def delete_user(self, id: int, db:Session=Depends(get_db))->dict:
        return UserRepository(db).delete(id) 

    def get_users(self,  offset: int = 0, limit: int = Query(default=100, le=100),  db:Session=Depends(get_db)):
        users = UserRepository(db).list(limit,offset)
        return users

        
    def create_user(self, user:UserCreate,  db:Session=Depends(get_db)):
        return UserRepository(db).create(user) or []
    
    def update_user(self, id:int,user_update:UserUpdate, db:Session=Depends(get_db)):
        return UserRepository(db).update(id, user_update) or []

    
