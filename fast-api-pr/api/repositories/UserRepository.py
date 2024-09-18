from typing import Any, List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..data.schemas import UserCreate,UserOut, UserUpdate
from ..data.models import User
from ..database import get_db 

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def list(
        self,
        limit: Optional[int]=100,
        start: Optional[int]=0,
        name: Optional[str]="",
    ) -> List[User]:
        query = self.db.query(User)

        if name:
            query = query.filter_by(name=name)
        
        return query.offset(start).limit(limit).all()  or []

    
    def get_by_name(self, username)->User:
        user = self.db.query(User).filter(User.email == username).first()    
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
        
    def get_by_id(self,user_id)->User|None:
        return self.db.query(User).filter(User.id == user_id).first() or None
    
    def create(self, user_create: UserCreate) -> User:
        db_user = User(**user_create.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    

    def delete(self, user_id) -> Any:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}
    
    def update(self, user_id: int, user_update: UserUpdate) -> User:
        db_user = (
            self.db.query(User).filter(
                User.id == user_id
            ).first()
        )
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        
        print(user_update.dict(exclude_unset=True))
        print("_________________"+str(user_id));     
        
        db_user.email = user_update.email
        db_user.hashed_password = User.hash(user_update.hashed_password)
        
        self.db.commit()
        self.db.refresh(db_user)
        
        print(user_update.dict(exclude_unset=True))

        return db_user
    
