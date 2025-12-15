import schemas, models
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db import get_db
import oauth2

router = APIRouter(
    prefix="/assignments",
    tags = ["assignments"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Assignment
)
def create_assignment(
        assignment: schemas.Assignment,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Create a new spot assignment."""
    # --- Error handling ---

    # Prevent assignment if there is an active break
    open_break = (
        db.query(models.Breaks)
        .filter(
            models.Breaks.shift_id == assignment.shift_id,
            models.Breaks.end_time.is_(None)
        )
        .first()
    )
    if open_break is not None:
        if open_break.end_time is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Guard currently on break"
            )

    # Prevent assignment to an occupied spot
    latest_spot_assignment = (
        db.query(models.Assignments)
        .filter(
            and_(
                models.Assignments.spot_id == assignment.spot_id,
                # Find if spot has an active assignment
                models.Assignments.active.is_(True),
            )
        )
        .first()
    )
    if latest_spot_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Spot already occupied"
        )

    # Prevent assignment if guard already has a spot
    active_assignment = (
        db.query(models.Assignments)
        .filter(
            and_(
                models.Assignments.shift_id == assignment.shift_id,
                models.Assignments.active.is_(True)
            )
        )
        .order_by(models.Assignments.time.desc())
        .first()
    )
    if active_assignment:
        if active_assignment.spot_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Guard actively assigned to a spot"
            )
        else:
            # Invalidate the active no-spot assignment
            active_assignment.active = False

    # --- Create and persist record ---

    new_assignment = models.Assignments(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment

@router.patch(
    "/replace/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Assignment
)
def replace_guard(
        id: int,
        new_assignment: schemas.Assignment,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Swap and create an existing guard's spot assignment."""
    # --- Retrieve current assignments ---

    # Active assignment of guard to be replaced
    old_guard = (
        db.query(models.Assignments)
        .join(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
        .join(models.Guards, models.Shifts.guard_id == models.Guards.id)
        .filter(
            and_(
                models.Guards.id == id,
                models.Assignments.active.is_(True)
            )
        )
        .first()
    )

    # Active assignment of replacement guard
    replacement_guard = (
        db.query(models.Assignments)
        .join(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
        .filter(
            and_(
                models.Shifts.id == new_assignment.shift_id,
                models.Assignments.active.is_(True)
            )
        )
        .first()
    )

    # --- Error handling ---

    # Prevent replacing no active assignment
    if not old_guard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Prevent assignment if guard on break
    replacement_guard_break = (
        db.query(models.Breaks)
        .join(models.Shifts, models.Breaks.shift_id == models.Shifts.id)
        .filter(
            models.Breaks.shift_id == new_assignment.shift_id,
            models.Breaks.end_time.is_(None)
        )
        .order_by(models.Breaks.end_time.desc())
        .first()
    )
    if replacement_guard_break is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Guard currently on break"
        )

    # --- Deactivate current assignments ---

    old_guard.active = False

    # Replacement guard may not currently be assigned to spot
    if replacement_guard is not None:
        replacement_guard.active = False

    db.flush()

    # --- Create and persist records ---

    # Set replacement guard's spot to the replaced guard's spot
    replacement_guard_assignment = (
        models.Assignments(**new_assignment.dict())
    )
    replacement_guard_assignment.spot_id = old_guard.spot_id

    # Create replaced guard's new assignment (no spot)
    old_guard_assignment = models.Assignments(
        shift_id=old_guard.shift_id,
        spot_id=None,
        time=new_assignment.time,
        active=True
    )

    db.add(old_guard_assignment)
    db.add(replacement_guard_assignment)
    db.commit()
    db.refresh(replacement_guard_assignment)

    return replacement_guard_assignment