from fastapi import FastAPI
from lifeguard_app.routers import guards, assignments, shifts, rotations, breaks
app = FastAPI()
app.include_router(guards.router)
app.include_router(assignments.router)
app.include_router(shifts.router)
app.include_router(rotations.router)
app.include_router(breaks.router)
@app.get("/")
async def root():
    return {"Message": "GG Aquatics"}