import os
from dotenv import load_dotenv

from src.messages.router import router as router_user_message
from src.auth.router import router as auth_router

from fastapi import FastAPI,Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


from src.auth.router import get_current_user

load_dotenv()

app = FastAPI()

app.include_router(router_user_message)
app.include_router(auth_router)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

templates = Jinja2Templates(directory="src/static/")


@app.get("/")
async def login(request: Request):
    """
    :param request: An instance of the `Request` class, representing the incoming HTTP request.
    :return: A TemplateResponse object rendering the "login.html" template with the given request context.
    """
    return templates.TemplateResponse("pages/login.html", {"request": request})


@app.get("/welcome")
async def welcome(request: Request, current_user: dict = Depends(get_current_user)):
    context = {"request": request, "name": current_user['name']}
    return templates.TemplateResponse("pages/welcome.html", context)


