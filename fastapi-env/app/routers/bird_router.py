from fastapi import APIRouter, HTTPException, Body, responses, status

from models.bird_model import Bird as BirdRepo
from schemas.bird import Bird 
import json

repo = BirdRepo()

router = APIRouter(
    prefix="/birds",
    tags=["Bird"],
    responses={404: {"Bird": "Not found"}},
)

@router.get("")
def get_all_birds():
    objects = repo.get_all()
    if objects is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return objects

@router.post("")
def create_bird(bird: Bird):
    new_bird = repo.create(bird)
    if new_bird is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return new_bird

@router.delete("/{id}")
def delete_bird(id: str):
    if repo.delete_bird(id):
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong here")

@router.get("/initialize")
def fill_database():
    with open("birds.json") as f:
        birds = json.load(f)
    for bird in birds:
        print("BIRD: ", bird)
        # convert bird to birdschema
        bird = Bird(**bird)
        repo.create(bird)
        if bird is None:
            raise HTTPException(status_code=400, detail="Something went wrong here")
    return birds

@router.put("/{id}")
def update_bird(id: str, bird: Bird):
    if repo.update_bird(id, bird):
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong here")

@router.get("/{id}")
def get_bird(id: str):
    bird = repo.get_by(id=id)
    if bird is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return bird

@router.get("{property}/{value}")
def get_birds_by_property(property: str, value: str):
    birds = repo.get_many_birds_based_on_property(property, value)
    if birds is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return birds


