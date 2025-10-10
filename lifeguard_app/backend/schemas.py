from pydantic import BaseModel
#stores all pydantic models used for sending data with HTTP requests

class Guard(BaseModel):
    first_name: str
    last_name: str

class Assignment(BaseModel):
    shift_id: int
    spot_id: int
    time: str

class ShiftClockIn(BaseModel):
    guard_id: int
    started_at: str

class ShiftClockOut(BaseModel):
    ended_at: str

class ShiftResponse(ShiftClockIn, ShiftClockOut):
    id: int

class BreakStart(BaseModel):
    guard_id: int
    type: int
    start_time: str

class BreakEnd(BaseModel):
    end_time: str

class BreakResponse(BreakStart, BreakEnd):
    id: int

class StatusResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    started_at: str
    rotation: str
    spot_name: str