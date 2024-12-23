from fastapi import FastAPI

from src.user_message.router import router as router_user_message

app = FastAPI()

app.include_router(router_user_message)