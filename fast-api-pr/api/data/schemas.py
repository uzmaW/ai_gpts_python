from email.mime import image
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, Union



# class User(BaseModel):
#     name : str
#     email: str
#     password: str



# User schemas
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
   
class UserBasic(UserBase):
   # firstname: str
   # lastname: str
    email: str
    
       
class User(UserBase):
    first_name: Optional[str] = Field(
        title="The name of the User to do",
        description="The name has a maximum length of 50 characters",
        max_length=50,
        examples = ["John doe"]
    )
    last_name: Optional[str] = Field(
        title="The name of the User to do",
        description="The name has a maximum length of 50 characters",
        max_length=50,
        examples = ["John doe"]
    )
    email : str = Field(
        title="The email of the user",
        description="The email has a maximum length of 50 characters",
        max_length=50,
        examples = ["user@gmail.com"]
    )
    # password: str
    created_at : datetime = datetime.now()
    role: str = 'user'
    is_superuser: Optional[bool] = False  # Default to False
    is_verified: Optional[bool] = False
    profile_picture: Optional[str] = Field(
        title="The profile picture of the user",
        description="The profile picture has a maximum length of 50 characters"
    )  
 
class UserCreate(User):
    hashed_password: str

class UserUpdate(BaseModel):
    hashed_password: str
    email: str
    updated_at: datetime = Field(default_factory=datetime.now)

class UserOut(User):
    id: int
    username: str = Field(..., alias="email")

class Todo(BaseModel):
    title: str
    description: str
    status: str

class TodoWithID(Todo):
    id: int
    user_id: int

class TodoWithUser(Todo):
    user: UserOut

class TodoUpdate(BaseModel):
    title:Optional[str] = None 
    description: Optional[str] = None
    status: str
    updated_at: datetime = Field(default_factory=datetime.now)

class TodoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title : str = Field(
        title="The title of the task",
        description="The title has a maximum length of 50 characters",
        max_length=50,
        examples = ["Buy milk"]
    )
    description : str = Field(
        title="The description of the task",
        description="The description has a maximum length of 50 characters",
        max_length=50,
        examples = ["Buy milk from the store"]
    )
    is_done : bool = Field(
        title="The status of the task",
        description="The status has a maximum length of 50 characters",
        examples = [False]
    )
    created_at : Optional[datetime] = None
    status: Optional[str] | None = None
 
    owner_id: Optional[int] | None = None

class TodoCreate(TodoBase):
    pass

class TodoStatusUpdate(BaseModel):
    is_done: bool
    completed_by: Optional[int] | None = None
    completed_at: Optional[datetime] | None = None


class TodoOut(TodoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_done: Optional[bool] = False
    description: Optional[str] = None
    title: Optional[str] = None
    

class UserOutWithTodos(UserOut):
    todos: list[TodoOut]

class TodoOutWithUser(TodoOut):
    user: UserOut
# class TodoDTO(BaseModel):
#     # id : int
#     title : str
#     description : str
#     user_id : int
#     created_at : Optional[date] = None
#     is_done: Optional[str] = None

#     class Config():
#         from_attributes = True


# class TodoUpdate:
#     title : Optional[str] = None
#     description : Optional[str] = None
#     updated_at : Optional[date] = None
#     is_done: Optional[str] = None

# #     class Config():
#         from_attributes = True

# class TodoDelete(TodoBase):
#    id: int
#    deleted_at: datetime = Field(default=None, alias="deletedAt")
#    deleted_by: int = Field(default=None, alias="deletedBy")

class TodoDeleteOut:
    msg: str    
    
# class Login(BaseModel):
#     email: str
#     password: str


# class Token(BaseModel):
#     access_token: str
#     user_id: int

#     class Config():
#         from_attributes = True
class TokenRequest(BaseModel):
    username: str = Field(
        title="The username of the user",
        description="The username has a maximum length of 50 characters",
        max_length=50,
        examples = ["John doe"]
    )
    password: str = Field(
        title="The password of the user",
        description="The password has a maximum length of 20 characters",
        max_length=20,
        examples = ["Justpass@"]
    )

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title : str = Field(
        title="The title of the task",
        description="The title has a maximum length of 50 characters",
        max_length=50,
        examples = ["Buy milk"]
    )
    description : str = Field(
        title="The description of the task",
        description="The description has a maximum length of 50 characters",
        max_length=50,
        examples = ["Buy milk from the store"]
    )
    is_done : bool = Field(
        title="The status of the task",
        description="The status has a maximum length of 50 characters",
        examples = [False]
    )
    created_at : Optional[datetime] = None
    status: Optional[str] | None = None
    updated_at: Optional[datetime] | None = None
    deleted_at: Optional[datetime] | None = None
    deleted_by: Optional[int] | None = None
    completed_by: Optional[int] | None = None
    completed_at: Optional[datetime] | None = None
    owner_id: Optional[int] | None = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    is_done: Optional[bool] = False
    description: Optional[str] = None
    title: Optional[str] = None
