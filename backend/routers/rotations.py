from collections import defaultdict
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from db import get_db
import models
import oauth2

router = APIRouter(prefix="/rotations", tags=["rotations"])

@router.get("/")
def get_rotations(
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Return data of all spots for all rotations."""
    # --- Retrieve rotations ---

    rotations = db.query(models.Rotations).all()

    # --- Retrieve spots ---

    # Select data of the spot with the most recent assignment
    spots = (
        db.query(
            models.Spots.rotation_id,
            models.Spots.id,
            models.Spots.order,
            models.Spots.name,
            func.concat_ws(
                ' ',
                models.Guards.first_name,
                models.Guards.last_name
            )
            .label('guard_name'),
            models.Spots.is_active
        )
        .outerjoin(models.Assignments, models.Spots.id == models.Assignments.spot_id)
        .outerjoin(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
        .outerjoin(models.Guards, models.Shifts.guard_id == models.Guards.id)
        .distinct(models.Spots.id) # one spot per spot id
        .order_by(models.Spots.id, models.Assignments.time.desc()) # most recent assignment
        .all()
    )

    # Group spots by rotation
    spots_by_rotation = defaultdict(list)
    for spot in spots:
        spots_by_rotation[spot.rotation_id].append(
            {
                "order": spot.order,
                "id": spot.id,
                "name": spot.name,
                "current_guard": spot.guard_name,
                "is_active": spot.is_active
            }
        )

    # --- Build and return response ---

    return [
        {
            "rotation_id": r.id,
            "name": r.name,
            "spots": spots_by_rotation.get(r.id,[])
        }
        for r in rotations
    ]

@router.get("/available_spots")
def get_available_spots(
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Returns available spots for all rotations."""
    # --- Retrieve rotations ---

    rotations = db.query(models.Rotations).all()

    # --- Retrieve available spots ---

    available_spots = (
        db.query(models.Spots)
        .outerjoin(
            models.Assignments,
            and_(
                models.Spots.id == models.Assignments.spot_id,

                # only select actively assigned spots
                models.Assignments.active.is_(True)
            )
        )
        # keep spots without an active assignment
        .filter(models.Assignments.id.is_(None))
        .order_by(models.Spots.order)
        .all()
    )

    # group spots by rotation
    spots_by_rotation = defaultdict(list)
    for spot in available_spots:
        spots_by_rotation[spot.rotation_id].append(spot)

    # --- Build and return response ---

    return [
        {
            "rotation_id": r.id,
            "name": r.name,
            "spots": spots_by_rotation.get(r.id,[])
        }
        for r in rotations
    ]