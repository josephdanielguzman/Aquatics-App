from fastapi import FastAPI
from .routers import shifts, rotations, breaks, guards, assignments
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(guards.router)
app.include_router(assignments.router)
app.include_router(shifts.router)
app.include_router(rotations.router)
app.include_router(breaks.router)

@app.get("/")
async def root():
    return {"Message": "GG Aquatics"}