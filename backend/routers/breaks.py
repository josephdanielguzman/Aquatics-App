import schemas, models
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from db import get_db
from datetime import datetime
import oauth2

router = APIRouter(prefix="/breaks", tags=["breaks"])

@router.post(
    "/",
    response_model=schemas.BreakResponse,
    status_code=status.HTTP_201_CREATED
)
def start_break(
        new_break: schemas.BreakStart,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Creates a new break for a guard."""
    # --- Validation and conflict checks ---

    # Check for breaks of this guard that are unfinished
    open_break = (
        db.query(models.Breaks)
        .filter(
            new_break.shift_id == models.Breaks.shift_id,
            models.Breaks.end_time.is_(None))
        .first()
    )

    # Check for existing break of the same type
    same_break = (
        db.query(models.Breaks)
        .filter(
        new_break.shift_id == models.Breaks.shift_id,
                new_break.type == models.Breaks.type)
        .first()
    )

    # Most recent break
    prev_break = (
        db.query(models.Breaks)
        .filter(new_break.shift_id == models.Breaks.shift_id)
        .order_by(models.Breaks.end_time.desc())
        .first()
    )

    # Check current spot assignment

    spot = (
        db.query(models.Assignments.spot_id)
        .join(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
        .filter(
            models.Shifts.id == new_break.shift_id,
            models.Assignments.active.is_(True)
        )
        .scalar()
    )

    # --- Error handling ---

    # Prevent duplicate break types
    if same_break:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Break already exists"
        )

    # Prevent starting a break while one is unfinished
    if open_break:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Previous break in progress"
        )

    # Prevent starting a break that overlaps with a previous one
    if prev_break:
        # Convert time to datetime objects
        prev_end_datetime = datetime.combine(
            datetime.today(),
            prev_break.end_time
        )
        new_start_datetime = datetime.combine(
            datetime.today(),
            new_break.start_time
        )
        diff_datetime = new_start_datetime - prev_end_datetime

        if diff_datetime.total_seconds() < 60:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Overlap with previous break"
            )

    # Prevent starting a break if the guard is at a spot
    if spot:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Guard currently at a spot"
        )

    # --- Create and persist new record ---

    new_break = models.Breaks(**new_break.dict())
    db.add(new_break)
    db.commit()
    db.refresh(new_break)

    return new_break

@router.patch("/end_break/{id}", response_model=schemas.BreakResponse)
def end_break(
        id: int,
        break_end: schemas.BreakEnd,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Updates the end time of an existing break given the break id."""
    # --- Retrieve target record ---

    update_break = (
        db.query(models.Breaks)
        .filter(models.Breaks.id == id, models.Breaks.end_time.is_(None))
        .first()
    )

    # --- Error handling --

    # Prevent updating a non-existent break
    if not update_break:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Break not found"
        )

    # --- Duration Validation ---

    # Converts times to datetime objects and calculates break duration
    start_datetime = datetime.combine(datetime.today(), update_break.start_time)
    end_datetime = datetime.combine(datetime.today(), break_end.end_time)
    duration_datetime = (end_datetime - start_datetime).total_seconds() / 60

    # Prevents finishing break in < 10 minutes or lunch in < 30 minutes
    if duration_datetime < 10 and update_break.type != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Break less than 10 minutes"
        )


    # Prevents finishing a lunch in < 30 minutes
    if duration_datetime < 30 and update_break.type == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lunch less than 30 minutes"
        )


    # --- Update and persist changes ---

    # Update value from schema
    for key, value in break_end.dict(exclude_unset=True).items():
        setattr(update_break, key, value)

    db.commit()
    db.refresh(update_break)

    return update_break
