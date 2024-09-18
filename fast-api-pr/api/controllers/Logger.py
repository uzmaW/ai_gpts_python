
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends


class Logger:
    def log(self, message: str, db: Session = Depends(get_db)):
        db.add(message)
        
    