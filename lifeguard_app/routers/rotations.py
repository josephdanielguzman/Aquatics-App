from .. import models, schemas
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/rotations", tags=["rotations"])

@router.get("/{id}")
def get_guards_on_rotation(id: int, db: Session = Depends(get_db)):
    pass

@router.post("/{id}/rotate")
def rotate():
    pass