import jwt
from datetime import datetime, timedelta, UTC
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    """Creates and returns an access token given data.
    Args:
        data (dict): JSON data corresponding to an access token.
    Returns:
        Encoded JWT token.
    """
    to_encode = data.copy()

    expire = (
            datetime.now(UTC)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """Verifies if the access token provided is valid.
    Args:
        token (string): JWT token.
    Returns:
        Decoded JWT token.
    """
    try:
        # decode and unpack token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")

        # missing token data
        if user_id is None or username is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=user_id, username=username)
    except jwt.PyJWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Token verification helper function."""
    credentials_exception = (
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    )

    return verify_access_token(token, credentials_exception)