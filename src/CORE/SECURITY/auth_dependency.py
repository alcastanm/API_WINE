from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.CORE.SECURITY.jwt_validator import verify_token

security = HTTPBearer()

def get_current_user(credentials = Depends(security)):

    token = credentials.credentials

    payload = verify_token(token)

    return payload