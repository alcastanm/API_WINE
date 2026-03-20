from jose import jwt, JWTError
from fastapi import HTTPException
from datetime import datetime, timezone
from src.CORE.SECURITY.security_config import SECRET_KEY, ALGORITHM



def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        exp = payload.get("exp")

        if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")