from fastapi import FastAPI
import database as db

from models.bird_model import Bird
from models.user_model import User

app = FastAPI()
db.start_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}

from routers import (
    bird_router as bird, # Just to make an alias, because it looks nicer.
    user_router as user
)

app.include_router(bird.router)
app.include_router(user.router)