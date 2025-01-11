import os
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from dotenv import load_dotenv

from google.auth.transport.requests import Request as AuthRequest

load_dotenv()

router = APIRouter(prefix='/api/authentication', tags=['auth'])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=openid email profile"

    return RedirectResponse(url=google_auth_url)


@router.get("/callback")
async def auth_callback(code: str, request: Request):
    token_request_uri = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': request.url_for('auth_callback'),
        'grant_type': 'authorization_code',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_request_uri, data=data)
        response.raise_for_status()
        token_response = response.json()

    id_token_value = token_response.get('id_token')
    if not id_token_value:
        raise HTTPException(status_code=400, detail="Missing id_token in response.")

    try:
        id_info = id_token.verify_oauth2_token(id_token_value, AuthRequest(), GOOGLE_CLIENT_ID, clock_skew_in_seconds=3)

        user_id = id_info['sub']
        name = id_info.get('name')
        request.session['user_id'] = user_id
        request.session['user_name'] = name

        return RedirectResponse(url=request.url_for('welcome'))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_current_user(request: Request) -> dict:
    user_name = request.session.get("user_name")
    if not user_name:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    user_id = request.session.get("user_id")

    return {"name": user_name, "user_id": user_id}
