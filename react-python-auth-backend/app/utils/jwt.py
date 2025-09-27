from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from app.core.config import settings

# Define the algorithm to be used for encoding and decoding the JWT
ALGORITHM = "HS256"
# Set the expiration time for the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload if "exp" in payload else None
    except JWTError:
        return None

def get_current_user(token: str) -> Optional[dict]:
    payload = verify_token(token)
    return payload if payload else None