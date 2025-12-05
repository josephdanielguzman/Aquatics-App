from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, utils, models
from db import get_db

router = APIRouter(prefix='/user', tags=['user'])

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
        user_credentials: schemas.UserCredentials,
        db: Session = Depends(get_db)
):
    """Creates a new user."""
    # --- Error handling ---

    # Empty fields
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty field(s)"
        )

    # Username already taken
    existing_user = (
        db.query(models.Users)
        .filter(models.Users.username == user_credentials.username)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username unavailable"
        )

    # --- Create record ---

    user_credentials.password = utils.hashify(user_credentials.password)
    new_user = models.Users(**user_credentials.dict())

    # --- Build and return response ---

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
