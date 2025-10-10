from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix="/rotations", tags=["rotations"])

@router.get("/{id}")
def get_guards_on_rotation(id: int, db: Session = Depends(get_db)):
    pass

@router.post("/{id}/rotate")
def rotate():
    pass