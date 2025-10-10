from lifeguard_app.backend import schemas, models
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix="/assignments", tags = ["assignments"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Assignment)
def create_assignment(assignment: schemas.Assignment, db: Session = Depends(get_db)):
    new_assignment = models.Assignments(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment
