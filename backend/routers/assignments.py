import schemas, models
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
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

    # Create old guard's new assignment (no spot)
    old_guard_assignment = models.Assignments(
        shift_id=old_guard.shift_id,
        spot_id=None,
        time=replacement_guard.time,
        active=True
    )

    # Deactivate old record for old guard
    old_guard.active = False

    db.add(old_guard_assignment)
    db.add(replacement_guard_assignment)
    db.commit()

    return replacement_guard_assignment