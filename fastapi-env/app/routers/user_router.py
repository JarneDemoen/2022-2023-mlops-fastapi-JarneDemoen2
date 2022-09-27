from fastapi import APIRouter, HTTPException, Body, responses, status

from models.user_model import User as UserRepo
from schemas.user import User

repo = UserRepo()

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"User": "Not found"}},
)

@router.get("")
def get_all_users():
    objects = repo.get_all()
    if objects is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return objects

@router.post("")
def create_user(user: User):
    new_user = repo.create(user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Something went wrong here")
    return new_user

@router.delete("/{id}")
def delete_user(id: str):
    if repo.delete_user(id):
        return responses.Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong here")