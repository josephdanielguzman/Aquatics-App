from lifeguard_app.backend import schemas, models
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from lifeguard_app.backend.db import get_db
from datetime import datetime, time, timedelta

#TODO: finish breaks endpoint

router = APIRouter(prefix="/breaks", tags=["breaks"])

@router.post("/", response_model=schemas.BreakResponse, status_code=status.HTTP_201_CREATED)
def start_break(new_break: schemas.BreakStart, db: Session = Depends(get_db)):
    """ Creates a new break. """
    new_break = models.Breaks(**new_break.dict())

    # break conflicts
    open_break = db.query(models.Breaks).filter(new_break.guard_id == models.Breaks.guard_id,
                                                models.Breaks.end_time.is_(None)).first()
    same_break = db.query(models.Breaks).filter(new_break.guard_id == models.Breaks.guard_id,
                                                new_break.type == models.Breaks.type).first()

    # prevent starting an already completed break
    if same_break:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Break already exists")

    # prevent starting a new break if an unfinished one exists
    if open_break:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Previous break in progress")

    db.add(new_break)
    db.commit()
    db.refresh(new_break)
    return new_break

@router.patch("/end_break/{id}", response_model=schemas.BreakResponse)
def end_break(id: int, break_end: schemas.BreakEnd, db: Session = Depends(get_db)):
    """ Updates the end time of an existing break given the id. """
    # break to be updated
    update_break = db.query(models.Breaks).filter(models.Breaks.id == id, models.Breaks.end_time.is_(None)).first()

    # break times conversion
    start_datetime = datetime.combine(datetime.today(), update_break.start_time )
    end_datetime = datetime.combine(datetime.today(), break_end.end_time)

    duration_datetime = (end_datetime - start_datetime).total_seconds() / 60

    # invalid break
    if duration_datetime < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Break less than 10 minutes")

    # break doesn't exist
    if not update_break:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Break not found")

    # update break data
    for key, value in break_end.dict(exclude_unset=True).items():
        setattr(update_break, key, value)

    db.commit()
    db.refresh(update_break)
    return update_break