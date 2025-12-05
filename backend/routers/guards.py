from collections import defaultdict
import models
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import func
import oauth2

router = APIRouter(prefix='/guards', tags=['Guards'])

@router.get("/on_shift")
def get_guard_status(
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Returns all necessary information of guards currently on shift."""
    # --- Retrieve guards on shift ---

    # All guards on shift and most recent spot assignment
    guards = (
        db.query(
            models.Guards.id,
            func.concat_ws(
                ' ',
                models.Guards.first_name,
                models.Guards.last_name
            )
            .label('name'),
            models.Shifts.id.label('shift_id'),
            models.Shifts.started_at.label('clock_in'),
            models.Shifts.ended_at.label('clock_out'),
            models.Rotations.name.label('rotation'),
            models.Spots.name.label('spot_name')
        )
        .join(models.Shifts, models.Guards.id == models.Shifts.guard_id)
        .outerjoin(models.Assignments, models.Shifts.id == models.Assignments.shift_id)
        .outerjoin(models.Spots, models.Assignments.spot_id == models.Spots.id)
        .outerjoin(models.Rotations, models.Spots.rotation_id == models.Rotations.id)
        .distinct(models.Guards.id) # single entry per guard
        .order_by(models.Guards.id, models.Assignments.id.desc()) # most recent assignment
        .all()
    )

    # --- Return empty array if no guards ---

    if not guards:
        return []

    # --- Retrieve breaks for guards ---

    guard_ids = [guard.id for guard in guards]
    breaks = (
        db.query(models.Breaks)
        .where(models.Breaks.guard_id.in_(guard_ids))
        .all()
    )

    # Group breaks by guard id
    breaks_by_guard = defaultdict(list)
    for b in breaks:
        breaks_by_guard[b.guard_id].append({
            "id": b.id,
            "type": b.type,
            "started": b.start_time,
            "ended": b.end_time
        })

    # --- Build and return response ---

    return [
        {
            "guard_id": g.id,
            "name": g.name,
            "shift_id": g.shift_id,
            "clock_in": g.clock_in,
            "clock_out": g.clock_out,
            "rotation": g.rotation,
            "spot_name": g.spot_name,
            "breaks": breaks_by_guard.get(g.id, [])
        }
        for g in guards
    ]

@router.get("/available")
def get_available_guards(
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Returns all guards currently not on shift."""
    # --- Retrieve guards not on shift ---

    guards = (
        db.query(
            models.Guards.id,func.concat_ws(
                ' ',
                models.Guards.first_name,
                models.Guards.last_name)
            .label('name')
        )
        .outerjoin(models.Shifts, models.Guards.id == models.Shifts.guard_id)
        .filter(models.Shifts.id.is_(None))
        .all()
    )

    # --- Error handling ---

    if not guards:
        return []

    # --- Build and return response ---

    return [
        {
            "id": g.id,
            "name": g.name
        }
        for g in guards
    ]