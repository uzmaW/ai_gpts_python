from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum
from passlib.apps import custom_app_context as pwd_context

class User(SQLModel, table=True):
    @staticmethod
    def hash(password: str):
        return pwd_context.hash(password)
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str
    role: str = Field(default="user")
    first_name: str = Field(nullable=True, index=True)
    last_name: str = Field(nullable=True, index=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    profile_picture: str = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    todos: List["Todo"] = Relationship(back_populates="owner")

class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    is_done: bool = False
    created_at: datetime = Field(default=datetime.now())
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True, nullable=True)
    owner: Optional[User] = Relationship(back_populates="todos")
    status: Optional[str] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
    completed_by: Optional[int] = None
    completed_at: Optional[datetime] = None

class JwtToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    access_token: str = Field(index=True)
    user_id: int = Field(index=True)

class Logger(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    action: str = Field(index=True)
    time: str = Field(index=True)
    ip: str = Field(index=True)
    data: str = Field(index=True)

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    is_done: bool = False
    created_at: datetime = Field(default=datetime.now())
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True, nullable=True)
    status: Optional[str] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
    completed_by: Optional[int] = None
    completed_at: Optional[datetime] = None

# class Oauth2Client(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True, nullable=True)
#     status: Optional[str] = None
#     client_id: Optional[str] = None
#     client_secret: Optional[str] = None
#     created_at: datetime = Field(default=datetime.now())
#     deleted_at: Optional[datetime] = None
#     deleted_by: Optional[int] = None

#Define a Python enum for device types
class DeviceType(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"

# class Oauth2Tokens(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     client_id: Optional[int] = Field(default=None, foreign_key="oauth2_client.id", index=True, nullable=True)
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True, nullable=True)
#     token: Optional[str] = None
#     refresh_token: Optional[str] = None
#     device_id: Optional[str] = None
#     created_at: datetime = Field(default=datetime.now())
#     expired_at: Optional[datetime] = None
#     device_type: Optional[DeviceType] = None

class Oauth2Clients(SQLModel, table=True):
    __tablename__ = "oauth2_clients"
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: str = Field(index=True, unique=True)
    client_secret: str
    redirect_uris: str  # This could be a JSON string or a comma-separated list
    grant_types: str  # This could also be a JSON string or a comma-separated list
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=True)

class Oauth2Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    access_token: str = Field(index=True, unique=True)
    refresh_token: Optional[str] = Field(default=None)
    expires_at: datetime
    client_id: str = Field(foreign_key="oauth2_clients.client_id")
    user_id: Optional[int] = Field(default=None)  # Assuming you have a user table
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Settings(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    key: str = Field(index=True)
    value: str = Field(index=True)
    session_group_id: int = Field(index=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
    status: Optional[str] = None

class Documents(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(index=True)
    file_path: str = Field(index=True)
    associate_id: Optional[int] = Field(default=None, foreign_key="task.id", index=True, nullable=True)
    entity_type: Optional[str] =  Field(default=None, nullable=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
    status: Optional[str] = None


    