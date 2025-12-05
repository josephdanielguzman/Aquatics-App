import schemas, models
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from .. import oauth2

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
        current_user: dict = Depends(oauth2.get_current_user)
):
    """Create a new spot assignment."""
    # -- Error handling --

    # Prevents double assignment
    # Find most recent assignment of spot
    latest_spot_assignment = (
        db.query(models.Assignments)
        .filter(models.Assignments.spot_id == assignment.spot_id)
        .order_by(models.Assignments.time.desc())
        .first()
    )

    # todo: only accounts for current day, needs modification for mult shifts
    if latest_spot_assignment:
        # Find the most recent assignment of that shift
        latest_assignment = (
            db.query(models.Assignments)
            .filter(models.Assignments.shift_id == latest_spot_assignment.shift_id)
            .order_by(models.Assignments.time.desc())
            .first()
        )

        # If the most recent assignment for the shift is the spot attempting to assign to, raise error
        if latest_spot_assignment.spot_id == latest_assignment.spot_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Spot currently occupied"
            )

    # -- Create and persist new record --

    new_assignment = models.Assignments(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment

@router.post(
    "/replace/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Assignment
)
def replace_guard(
        id: int,
        replacement_guard: schemas.Assignment,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Swap and create an existing guard's spot assignment."""
    # --- Retrieve target record ---

    # Assignment of guard whose spot is to be swapped with
    old_guard = (
        db.query(models.Assignments)
        .join(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
        .join(models.Guards, models.Shifts.guard_id == models.Guards.id)
        .filter(models.Guards.id == id)
        .order_by(models.Assignments.time.desc())
        .first()
    )

    # --- Error handling ---

    if not old_guard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # --- Create and persist records ---

    # Set new guard's spot to the old guard's spot
    replacement_guard_assignment = (
        models.Assignments(**replacement_guard.dict())
    )
    replacement_guard_assignment.spot_id = old_guard.spot_id

    # Create new record for old guard with no spot
    old_guard_assignment = models.Assignments(shift_id=old_guard.shift_id,
                                              spot_id=None,
                                              time=replacement_guard.time)

    db.add(replacement_guard_assignment)
    db.add(old_guard_assignment)
    db.commit()

    return replacement_guard_assignment