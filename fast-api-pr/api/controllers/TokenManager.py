from fastapi import APIRouter, HTTPException, status, Depends
from ..data.schemas import TokenRequest
from ..security.manage_jwt import create_access_token



class TokenManager:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/token"    , self.create_token, methods=["POST"])#,   response_model=TodoOut, 
    
    # Route to create a JWT token
    def create_token(self, token_request: TokenRequest):
        access_token = create_access_token(data={"sub": token_request.username})
        return {"access_token": access_token, "token_type": "bearer"}