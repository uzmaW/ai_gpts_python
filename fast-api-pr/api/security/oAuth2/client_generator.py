import hashlib
import json
import secrets
from fastapi import JSONResponse

class oAuth2Client:

    def generate_client_id(client_name: str) -> str:
        # Generate a unique client ID based on the client name
        # You can use a hash function or any other method
        return hashlib.sha256(client_name.encode()).hexdigest()

    def generate_client_secret() -> str:
        # Generate a random client secret
        return secrets.token_urlsafe(32)
    def generate_client(self, client_name: str)->json:
        return JSONResponse(content={'client':self.generate_client_id(client_name), 
                             'secret': self.generate_client_secret})
        
     
