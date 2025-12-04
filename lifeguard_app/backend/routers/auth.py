from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth',tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(
        user_info: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """Returns token upon successful login."""
     # --- Retrieve target record ---

    user = (
        db.query(models.Users)
        .filter(models.Users.username == user_info.username)
        .first()
    )

    # --- Error handling ---

    # User does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Incorrect password
    if not utils.verify_password(user_info.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # --- Build and return response ---

    # Create token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "username": user.username}
    )

    return access_token