from lifeguard_app.backend import schemas, models
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db

#TODO: finish breaks endpoint

router = APIRouter(prefix="/breaks", tags=["breaks"])

@router.post("/", response_model=schemas.BreakStart, status_code=status.HTTP_201_CREATED)
def start_break(new_break: schemas.BreakStart, db: Session = Depends(get_db)):
    new_break = models.Breaks(**new_break.dict())
    db.add(new_break)
    db.commit()
    db.refresh(new_break)
    return new_break

@router.post("/{id}:end-break", response_model=schemas.BreakResponse)
def end_break(id: int, break_end: schemas.BreakEnd, db: Session = Depends(get_db)):
    update_break = db.query(models.Breaks).filter(models.Breaks.id == id).first()

    if not update_break:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Break not found")

    update_break.end_time = break_end.end_time
    db.commit()
    db.refresh(update_break)
    return update_break
