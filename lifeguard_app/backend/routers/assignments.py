from lifeguard_app.backend import schemas, models
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix="/assignments", tags = ["assignments"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Assignment)
def create_assignment(assignment: schemas.Assignment, db: Session = Depends(get_db)):

    # -- Error handling --

    # Prevents double assignment
    # Find most recent assignment of spot
    latest_spot_assignment = (db.query(models.Assignments)
                              .filter(models.Assignments.spot_id == assignment.spot_id)
                              .order_by(models.Assignments.time.desc())
                              .first())

    # todo: only accounts for current day, needs modification for mult shifts
    if latest_spot_assignment:
        # Find most recent assignment of that shift
        latest_assignment = (db.query(models.Assignments)
                             .filter(models.Assignments.shift_id == latest_spot_assignment.shift_id)
                             .order_by(models.Assignments.time.desc())
                             .first())

        # If the most recent assignment for the shift is the spot attempting to assign to, raise error
        if latest_spot_assignment.spot_id == latest_assignment.spot_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Spot currently occupied")

    # -- Create and persist new record --

    new_assignment = models.Assignments(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment
