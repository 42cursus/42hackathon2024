from fastapi import APIRouter, Request, Response
from pydantic import BaseModel as BM
router = APIRouter()

@router.get("/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


class RegisterValidator(BM):
    username: str

@router.post("/api/register")
def register_user(user: RegisterValidator, response: Response):
    response.set_cookie(
        key="X-Authorization",
        value=user.username,
        httponly=True,
        secure=True,
        samesite="none"
    )


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
