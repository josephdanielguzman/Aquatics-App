from pydantic import BaseModel
#stores all pydantic models used for sending data with HTTP requests

class GuardBase(BaseModel):
    first_name: str
    last_name: str

class UpdateGuard(GuardBase):
    pass

class Guard(BaseModel):
    first_name: str