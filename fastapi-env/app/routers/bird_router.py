from fastapi import APIRouter, HTTPException, Body, responses, status

from models.bird_model import Bird as BirdRepo
from schemas.bird import Bird 

repo = BirdRepo()

router = APIRouter(
    prefix="/birds",
    tags=["Bird"],
    responses={404: {"Bird": "Not found"}},
)

@router.get("/birds")
def get_all_birds():
    objects = repo.get_all()
    if objects is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return objects

@router.post("/birds")
def create_bird(bird: Bird):
    new_bird = repo.create(bird)
    if new_bird is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return new_bird

