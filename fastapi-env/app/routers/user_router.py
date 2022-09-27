from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"User": "Not found"}},
)