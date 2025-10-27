from lifeguard_app.backend import schemas, models
from fastapi import  Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix = "/shifts", tags = ["shifts"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShiftResponse)
def clock_in(shift: schemas.ShiftClockIn, db: Session = Depends(get_db)):
    """Create a new shift."""
    # --- Error handling ---

    # Prevent creating a new shift with one still unfinished
    open_shift = db.query(models.Shifts).filter(shift.guard_id == models.Shifts.guard_id).first()
    if open_shift:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guard already on shift.")

    # --- Create and persist new record ---

    new_shift = models.Shifts(**shift.dict())
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)

    return new_shift

@router.post("/{id}:clock-out", response_model=schemas.ShiftResponse)
def clock_out(id: int, shift: schemas.ShiftClockOut, db: Session = Depends(get_db)):
    """End the shift of a given id."""
    # --- Retrieve target record ---

    # Shift to be ended
    update_shift = db.query(models.Shifts).filter(models.Shifts.id == id).first()

    # --- Error handling ---

    # Prevent ending a shift that does not exist
    if not update_shift:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Shift {id} not found")

    # --- Update and persist changes ---

    update_shift.ended_at = shift.ended_at
    db.commit()
    db.refresh(update_shift)

    return update_shift