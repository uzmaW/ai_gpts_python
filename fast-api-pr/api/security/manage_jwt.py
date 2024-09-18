from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..settings import Settings as settings
from ..controllers.Users import Users
from ..data.schemas import UserOut
from ..data.models import User

# Dependency to get the current user based on the JWT token
def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")))->dict|UserOut:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data= Users.get_by_name(username)
    if not user_data:
        raise credentials_exception
    user = UserOut(
            first_name=user_data.first_name,
            last_name=user_data.last_name, 
            username=user_data.email, 
            created_at=user_data.created_at,
            id=user_data.id,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
            is_verified=user_data.is_verified,
            updated_at=user_data.updated_at,
            profile_picture=user_data.profile_picture)
            
    if username != user.email:
        raise credentials_exception

    return user

# Function to create a JWT token
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def create_access_token(data: dict):
    if 'username' not in data or 'password' not in data:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(data={"sub": data['username']}, expires_delta=expires_delta)

    return {"access_token": access_token, "token_type": "bearer"}