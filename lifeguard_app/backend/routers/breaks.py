from lifeguard_app.backend import schemas, models
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db
from datetime import datetime

router = APIRouter(prefix="/breaks", tags=["breaks"])

@router.post("/", response_model=schemas.BreakResponse, status_code=status.HTTP_201_CREATED)
def start_break(new_break: schemas.BreakStart, db: Session = Depends(get_db)):
    """Creates a new break for a guard."""

    # --- Validation and conflict checks ---

    # todo: limit scope to today, currently prevents even if taken on another day
    # Check for breaks of this guard that are unfinished
    open_break = db.query(models.Breaks).filter(
        new_break.guard_id == models.Breaks.guard_id,
                models.Breaks.end_time.is_(None)).first()

    # Check for existing break of the same type
    same_break = (db.query(models.Breaks).filter(
        new_break.guard_id == models.Breaks.guard_id,
                new_break.type == models.Breaks.type).first())

    # --- Error handling ---

    # Prevent duplicate break types
    if same_break:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Break already exists")

    # Prevent starting a break while one is unfinished
    if open_break:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Previous break in progress")

    # --- Create and persist new record ---
    new_break = models.Breaks(**new_break.dict())
    db.add(new_break)
    db.commit()
    db.refresh(new_break)

    return new_break

@router.patch("/end_break/{id}", response_model=schemas.BreakResponse)
def end_break(id: int, break_end: schemas.BreakEnd, db: Session = Depends(get_db)):
    """Updates the end time of an existing break given the break id."""

    # --- Retrieve target record ---
    update_break = db.query(models.Breaks).filter(models.Breaks.id == id, models.Breaks.end_time.is_(None)).first()

    # --- Error handling --

    # Prevent updating a non-existent break
    if not update_break:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Break not found")

    # --- Duration Validation ---

    # Converts times to datetime objects and calculates break duration
    start_datetime = datetime.combine(datetime.today(), update_break.start_time)
    end_datetime = datetime.combine(datetime.today(), break_end.end_time)
    duration_datetime = (end_datetime - start_datetime).total_seconds() / 60

    # Prevents finishing break in < 10 minutes
    if duration_datetime < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Break less than 10 minutes")

    # --- Update and persist changes ---

    # Update value from schema
    for key, value in break_end.dict(exclude_unset=True).items():
        setattr(update_break, key, value)

    db.commit()
    db.refresh(update_break)

    return update_break
