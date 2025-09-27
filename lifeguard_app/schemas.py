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
    pass