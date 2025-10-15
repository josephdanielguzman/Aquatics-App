from collections import defaultdict
from http.client import HTTPException
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db
from lifeguard_app.backend import models
router = APIRouter(prefix="/rotations", tags=["rotations"])

@router.get("/")
def get_rotations(db: Session = Depends(get_db)):
    rotations = db.query(models.Rotations).all()

    spots = ((((db.query(models.Spots.rotation_id,
                     models.Spots.order,
                     models.Spots.name,
                     models.Guards.first_name.label('guard_first_name'),
                     models.Guards.last_name.label('guard_last_name'),
                     models.Spots.is_active)
             .outerjoin(models.Assignments, models.Spots.id == models.Assignments.spot_id))
             .outerjoin(models.Shifts, models.Assignments.shift_id == models.Shifts.id))
             .outerjoin(models.Guards, models.Shifts.guard_id == models.Guards.id))
             .order_by(models.Spots.order).all())

    spots_by_rotation = defaultdict(list)

    for spot in spots:
        spots_by_rotation[spot.rotation_id].append({
            "order": spot.order,
            "name": spot.name,
            # TODO: fix "None None" when a spot doesnt have a guard
            "current_guard": f"{spot.guard_first_name} {spot.guard_last_name}",
            "is_active": spot.is_active

        })

    return [
        {
            "rotation_id": r.id,
            "name": r.name,
            "spots": spots_by_rotation.get(r.id,[])
        }
        for r in rotations
    ]


@router.get("/{id}")
def get_guards_on_rotation(id: int, db: Session = Depends(get_db)):
    spots = db.query(models.Spots.name,
                     models.Spots.order,
                     models.Spots.is_active).filter(models.Spots.rotation_id == id).all()

    if not spots:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rotation with Id {id} not found")

    return [
        {
        "order": spot.order,
        "spot_name": spot.name,
        "is_active": spot.is_active
        }
        for spot in spots
    ]

@router.post("/{id}/rotate")
def rotate():
    pass