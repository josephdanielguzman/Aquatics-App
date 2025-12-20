from collections import defaultdict
import models
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import func, or_, and_
import oauth2

router = APIRouter(prefix='/guards', tags=['Guards'])

@router.get("/on_shift")
def get_guard_status(
        guard_id: int | None = Query(default=None),
        db: Session = Depends(get_db),
        user: dict = Depends(oauth2.get_current_user)
):
    """Returns all necessary information of guards currently on shift."""
    # --- Retrieve guards on shift ---

    # All guards on shift and most recent spot assignment
    guards_query = (
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
            models.Rotations.id.label('rotation_id'),
            models.Spots.name.label('spot_name'),
            models.Spots.id.label('spot_id'),
        )
        .join(models.Shifts,
              and_(
                  # only include unfinished shifts
                  models.Guards.id == models.Shifts.guard_id,
                  models.Shifts.ended_at.is_(None)
              )
        )
        .outerjoin(models.Assignments, models.Shifts.id == models.Assignments.shift_id)
        .outerjoin(models.Spots, models.Assignments.spot_id == models.Spots.id)
        .outerjoin(models.Rotations, models.Spots.rotation_id == models.Rotations.id)
        .distinct(models.Guards.id) # single entry per guard
        .order_by(models.Guards.id, models.Assignments.id.desc()) # most recent assignment
    )

    if guard_id is not None:
        guards_query = guards_query.filter(models.Guards.id == guard_id)

    guards = guards_query.all()

    # --- Return empty array if no guards ---

    if not guards:
        return []

    # --- Retrieve breaks for guards ---

    shift_ids = [guard.shift_id for guard in guards]
    breaks = (
        db.query(models.Breaks)
        .where(models.Breaks.shift_id.in_(shift_ids))
        .all()
    )

    # Group breaks by guard id
    breaks_by_guard = defaultdict(list)
    for b in breaks:
        breaks_by_guard[b.shift_id].append({
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
            "rotation_id": g.rotation_id,
            "spot_name": g.spot_name,
            "spot_id": g.spot_id,
            "breaks": breaks_by_guard.get(g.shift_id, [])
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

@router.get("/on_shift/no_spot")
def get_guards_no_spot(
        db: Session = Depends(get_db),
        current_user: dict = Depends(oauth2.get_current_user)
):
    """Returns all guards on shift that are not assigned to a spot and not on an unfinished break."""

    # Subquery: get the most recent break id for each shift
    latest_break_subq = (
        db.query(
            models.Breaks.shift_id,
            func.max(models.Breaks.id).label('max_break_id')
        )
        .group_by(models.Breaks.shift_id)
        .subquery()
    )

    # Subquery: shifts with an unfinished break (end_time IS NULL on most recent break)
    shifts_with_unfinished_break = (
        db.query(models.Breaks.shift_id)
        .join(
            latest_break_subq,
            and_(
                models.Breaks.shift_id == latest_break_subq.c.shift_id,
                models.Breaks.id == latest_break_subq.c.max_break_id
            )
        )
        .filter(models.Breaks.end_time.is_(None))
        .subquery()
    )

    # Main query: guards on shift with no spot (or no assignments) and no unfinished break
    guards = (
        db.query(
            models.Guards.id,
            func.concat_ws(
                ' ',
                models.Guards.first_name,
                models.Guards.last_name
            ).label('name')
        )
        .join(models.Shifts, models.Guards.id == models.Shifts.guard_id)
        .filter(models.Shifts.ended_at.is_(None))  # Only guards currently on shift
        .outerjoin(
            models.Assignments,
            and_(
                models.Shifts.id == models.Assignments.shift_id,
                models.Assignments.active.is_(True)
            )
        )
        .filter(
            or_(
                models.Assignments.id.is_(None),      # No assignments at all
                models.Assignments.spot_id.is_(None)  # Active assignment with no spot
            )
        )
        .filter(~models.Shifts.id.in_(shifts_with_unfinished_break))  # Exclude unfinished breaks
        .all()
    )

    if not guards:
        return []

    return [
        {
            "id": g.id,
            "name": g.name
        }
        for g in guards
    ]