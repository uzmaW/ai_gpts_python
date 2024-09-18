
from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List
from ..data.schemas import TodoCreate, TodoUpdate, TodoOut
from ..data.models import Todo
from ..repositories.TodoRepository import TodoRepository
from typing import Optional,Any

from sqlalchemy.orm import Session
from ..database import get_db

class Todos:
    
    def __init__(self):
        self.router = APIRouter(prefix="/todos", tags=["todo"])
        self.router.add_api_route("/"    , self.get_todos,   methods=["GET"],    response_model=List[TodoOut])
        self.router.add_api_route("/add"    , self.create_todo, methods=["POST"],   response_model=TodoOut, 
                                                                             status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/{id}", self.get_todo,    methods=["GET"],    response_model=TodoOut)
        self.router.add_api_route("/{id}", self.update_todo, methods=["PUT"],    response_model=TodoOut)
        self.router.add_api_route("/{id}", self.delete_todo, methods=["DELETE"]) 
    
        
    def get_todos(self, 
        offset: int = 0, 
        limit: int = Query(default=100, le=100),
        name: str="",
        db: Session = Depends(get_db)
    ) -> List[Todo]:
        
        return TodoRepository(db).list(limit, offset, name)
        
    def get_todo(self, todo_id: int, db:Session=Depends(get_db)) -> Todo: #TodoBase:
        return TodoRepository(db).get(todo_id)    
    
    def create_todo(self, todo: TodoCreate, db: Session = Depends(get_db)):
        return TodoRepository(db).create(todo)
    
    def update_todo(self,todo_id:int, todo_update:TodoUpdate , db: Session = Depends(get_db)):
        return TodoRepository(db).update(todo_id,todo_update)
    
    def delete_todo(self, todo_id: int, db: Session = Depends(get_db)) -> Any:
        """
        Delete a todo
        """
        return TodoRepository(db).delete(todo_id)

    
