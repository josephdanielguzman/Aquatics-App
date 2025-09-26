from .. import models, schemas
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import

router = APIRouter(prefix='/guards', tags=['Guards'])

# DONE
@router.get("/")
def get_guards(db: Session = Depends(get_db)):
    guards = db.query(models.Guards).all()
    return guards

# DONE
@router.get("/{id}")
def get_guard(id: int, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id).first()
    if not guard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    return guard

@router.get("/{id}/spot")
def get_current_spot(guard_id: int, db: Session = Depends(get_db)):

# DONE
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Guard)
def create_guard(guard: schemas.GuardBase, db: Session = Depends(get_db)):
    new_guard = models.Guards(**guard.dict())
    db.add(new_guard)
    db.commit()
    db.refresh(new_guard)
    return new_guard

# Done
@router.put("/{id}")
def update_guard(id: int, updated_guard: schemas.UpdateGuard, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id)

    if not guard.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    guard.update(updated_guard.dict(), synchronize_session=False)
    db.commit()

    return guard.first()

# DONE
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_guard(id: int, db: Session = Depends(get_db)):
    guard = db.query(models.Guards).where(models.Guards.id == id)

    if not guard.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guard not found")

    guard.delete(synchronize_session = False)
    db.commit()
