from typing import List, Optional, Any
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..data.models import Todo
from ..database import get_db 
from ..data.schemas import TodoBase,TodoUpdate

class TodoRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def list(
        self,
        limit: Optional[int] = 100,
        start: Optional[int] = 0,
        title = "",
    ) -> List[Todo]:
        query = self.db.query(Todo)

        if title:  # Check if name is provided
            query = query.filter_by(title = title)  # Use filter for explicit condition

        return query.offset(start).limit(limit).all()
    
    def get(self, todo_id) -> Todo:
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo 
    
    def create(self, todo_create: TodoBase) -> Todo:
        db_item = Todo(**todo_create.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete(self, todo_id) -> str:
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.db.delete(todo)
        self.db.commit()
        return {"message": "Todo deleted successfully"}
    
    def update(self, todo_id, todo_update: TodoUpdate) -> Todo:
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        for key, value in todo_update.dict(exclude_unset=True).items():
            setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo

