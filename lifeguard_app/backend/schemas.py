from pydantic import BaseModel, field_validator, BeforeValidator
from datetime import time, datetime
from typing import Any, Annotated

def parse_time_string(v: Any) -> time:
    """Parse time strings into time objects"""
    if isinstance(v, str):
        for fmt in ['%I:%M %p', '%H:%M', '%I:%M%p']:
            try:
                return datetime.strptime(v, fmt).time()
            except ValueError:
                continue
        raise ValueError(f'Invalid time format: {v}')
    return v

TimeField = Annotated[time, BeforeValidator(parse_time_string)]

class Guard(BaseModel):
    first_name: str
    last_name: str

class Assignment(BaseModel):
    shift_id: int
    spot_id: int | None
    time: TimeField

class ShiftClockIn(BaseModel):
    guard_id: int
    started_at: TimeField

class ShiftClockOut(BaseModel):
    ended_at: TimeField | None

class ShiftResponse(ShiftClockIn, ShiftClockOut):
    id: int

class BreakStart(BaseModel):
    guard_id: int
    type: int
    start_time: TimeField

class BreakEnd(BaseModel):
    end_time: TimeField | None

class BreakResponse(BreakStart, BreakEnd):
    id: int

class StatusResponse(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    clock_in: TimeField
    rotation: str
    spot_name: str

class RotationsResponse(BaseModel):
    id: int
    rotation_name: str
    spot_name:str
