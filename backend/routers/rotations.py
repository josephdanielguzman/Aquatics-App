from collections import defaultdict
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from db import get_db
import models
import oauth2
import schemas

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

    # Select active assignment for all spots if it exists
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
        .outerjoin(
            models.Assignments,
                   and_(
                       models.Spots.id == models.Assignments.spot_id,
                       models.Assignments.active.is_(True)
                   )
        )
        .outerjoin(
            models.Shifts,
            models.Assignments.shift_id == models.Shifts.id
        )
        .outerjoin(models.Guards, models.Shifts.guard_id == models.Guards.id)
        .order_by(models.Spots.order)
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

@router.post("/{rotation_id}/rotate", status_code=status.HTTP_201_CREATED)
def rotate_guards(
        rotation_id: int,
        new_rotation: schemas.Rotate,
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Rotate all guards in a rotation to the next spot."""

    # --- Get all spots in rotation ---
    
    spots = (
        db.query(models.Spots)
        .filter(models.Spots.rotation_id == rotation_id)
        .order_by(models.Spots.order)
        .all()
    )

    # --- Get current guard assignments for each spot ---
    
    # Map spot_id -> shift_id of the guard currently at that spot
    spot_to_guard = {}
    
    for spot in spots:
        # Get active assignment for this spot
        assignment = (
            db.query(models.Assignments)
            .filter(
                and_(
                    models.Assignments.spot_id == spot.id,
                    models.Assignments.active.is_(True)
                )
            )
            .order_by(models.Assignments.time.desc())
            .first()
        )
        
        if assignment:
            spot_to_guard[spot.id] = assignment.shift_id
        else:
            spot_to_guard[spot.id] = None  # Empty spot
    
    # --- Create rotation mapping (current spot -> next spot) ---
    
    # Build the rotation: each guard moves to the next spot
    rotation_mapping = {}
    for i in range(len(spots)):
        current_spot = spots[i]
        next_spot = spots[(i + 1) % len(spots)]  # Wrap around to first spot
        rotation_mapping[current_spot.id] = next_spot.id
    
    # --- Deactivate current assignments for guards in rotation ---
    
    shift_ids_in_rotation = [shift_id for shift_id in spot_to_guard.values() if shift_id is not None]
    
    if shift_ids_in_rotation:
        db.query(models.Assignments).filter(
            and_(
                models.Assignments.shift_id.in_(shift_ids_in_rotation),
                models.Assignments.active.is_(True)
            )
        ).update({"active": False}, synchronize_session=False)
        
        db.flush()
    
    # --- Create new assignments for rotated guards ---

    new_assignments = []
    
    for current_spot_id, next_spot_id in rotation_mapping.items():
        shift_id = spot_to_guard[current_spot_id]
        
        # Only create assignment if there's a guard at this spot
        if shift_id is not None:
            new_assignment = models.Assignments(
                shift_id=shift_id,
                spot_id=next_spot_id,
                time=new_rotation.time,
                active=True
            )
            new_assignments.append(new_assignment)
    
    # --- Persist all changes ---
    
    if new_assignments:
        db.add_all(new_assignments)
    
    db.commit()
    
    # --- Build and return response ---
    
    return {
        "rotation_id": rotation_id,
        "rotated_guards": len(new_assignments),
    }
