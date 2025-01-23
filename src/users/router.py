from fastapi import APIRouter, Request, HTTPException
from watchfiles import awatch

from src.users.dao import UserDAO


router = APIRouter(prefix='/api/user', tags=['ApiUsers'])


@router.post('/save')
async def save_google_user(username, email):
    user_info = {
        'username': username,
        'email': email
    }
    await UserDAO.add(**user_info)

    return {'message': 'User saved!'}

async def get_current_user(request: Request) -> dict:
    username = request.session.get("username")
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    user = await UserDAO.find_one_or_none(username=username)
    print("===========================================")
    print(user)
    user_id = user.id

    return {"username": username, "user_id": user_id}