from collections import defaultdict

from lifeguard_app.backend import schemas, models
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

router = APIRouter(prefix='/guards', tags=['Guards'])

@router.get("/")
def get_guards(db: Session = Depends(get_db)):
    guards = db.query(models.Guards).all()
    return guards

@router.get("/status")
def get_guard_status(db: Session = Depends(get_db)):
    guards = (db.query(models.Guards.id,
                      models.Guards.first_name,
                      models.Guards.last_name,
                      models.Shifts.started_at,
                      models.Rotations.name.label("rotation"),
                      models.Spots.name.label("spot_name"))
              .join(models.Shifts, models.Guards.id == models.Shifts.guard_id)
              .join(models.Assignments, models.Shifts.id == models.Assignments.shift_id)
              .join(models.Spots, models.Assignments.spot_id == models.Spots.id)
              .join(models.Rotations, models.Spots.rotation_id == models.Rotations.id)
              .all())

    guard_ids = [guard.id for guard in guards]

    # TODO: update table to use shift id instead of guard id
    breaks = db.query(models.Breaks).where(models.Breaks.guard_id.in_(guard_ids)).all()

    breaks_by_guard = defaultdict(list)

    # creates dict with guard id:breaks
    for b in breaks:
        breaks_by_guard[b.guard_id].append({
            "type": b.type,
            "started": b.start_time,
            "ended": b.end_time
        })

    return [
        {
            "id": g.id,
            "first_name": g.first_name,
            "last_name": g.last_name,
            "rotation": g.rotation,
            "spot_name": g.spot_name,
            "breaks": breaks_by_guard.get(g.id, [])
        }
        for g in guards
    ]

@router.get("/{id}")
def get_guard(id: int, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id).first()
    if not guard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    return guard

@router.get("/{id}/spot")
def get_current_spot(id: int, db: Session = Depends(get_db)):
    spot = (db.query(models.Spots.name)
            .join(models.Assignments, models.Assignments.spot_id == models.Spots.id)
            .join(models.Shifts, models.Assignments.shift_id == models.Shifts.id)
            .filter(models.Shifts.guard_id == id).scalar())

    if not spot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found")

    return spot

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Guard)
def create_guard(guard: schemas.Guard, db: Session = Depends(get_db)):
    new_guard = models.Guards(**guard.dict())
    db.add(new_guard)
    db.commit()
    db.refresh(new_guard)
    return new_guard

@router.put("/{id}")
def update_guard(id: int, updated_guard: schemas.Guard, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id)

    if not guard.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    guard.update(updated_guard.dict(), synchronize_session=False)
    db.commit()

    return guard.first()

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_guard(id: int, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id)

    if not guard.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    guard.delete(synchronize_session = False)
    db.commit()