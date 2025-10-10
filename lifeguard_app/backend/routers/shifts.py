from lifeguard_app.backend import schemas, models
from fastapi import  Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix = "/shifts", tags = ["shifts"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShiftClockIn)
def clock_in(shift: schemas.ShiftClockIn, db: Session = Depends(get_db)):
    new_shift = models.Shifts(**shift.dict())
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift

@router.post("/{id}:clock-out", response_model=schemas.ShiftResponse)
def clock_out(id: int, shift: schemas.ShiftClockOut, db: Session = Depends(get_db)):
    update_shift = db.query(models.Shifts).filter(models.Shifts.id == id).first()

    if not update_shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Shift {id} not found")

    update_shift.ended_at = shift.ended_at
    db.commit()
    db.refresh(update_shift)
    return update_shift

#TODO: implement patch for supervisor time edits