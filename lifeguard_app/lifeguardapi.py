from fastapi import FastAPI
from lifeguard_app.routers import guards, assignments, shifts, rotations
app = FastAPI()
app.include_router(guards.router)
app.include_router(assignments.router)
app.include_router(shifts.router)
app.include_router(rotations.router)
@app.get("/")
async def root():
    return {"Message": "GG Aquatics"}