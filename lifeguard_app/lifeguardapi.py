from fastapi import FastAPI
from . import models
from .db import engine
from lifeguard_app.routers import guard

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(guard.router)

@app.get("/")
async def root():
    return {"Message": "GG Aquatics"}