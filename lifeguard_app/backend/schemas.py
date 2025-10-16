from pydantic import BaseModel, field_validator
from datetime import time

class Guard(BaseModel):
    first_name: str
    last_name: str

class Assignment(BaseModel):
    shift_id: int
    spot_id: int
    time: time

class ShiftClockIn(BaseModel):
    guard_id: time
    started_at: time

class ShiftClockOut(BaseModel):
    ended_at: time

class ShiftResponse(ShiftClockIn, ShiftClockOut):
    id: int

class BreakStart(BaseModel):
    guard_id: int
    type: int
    start_time: time

class BreakEnd(BaseModel):
    end_time: time

class BreakResponse(BreakStart, BreakEnd):
    id: int

class StatusResponse(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    clock_in: time
    rotation: str
    spot_name: str

class RotationsResponse(BaseModel):
    id: int
    rotation_name: str
    spot_name:str