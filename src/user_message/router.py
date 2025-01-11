from fastapi import APIRouter, Depends

from src.celery_app import app as celery_app, redis_client

from src.storage import collection
from src.auth.router import get_current_user
from src.user_message.schemas import TestData
from src.user_message.dao import UsersMessageDAO

router = APIRouter(prefix='/api', tags=['Api'])


@router.post('/submit')
async def get_json(data: TestData | None = None, current_user: dict = Depends(get_current_user)):
    user_message = data.dict()
    user_message.update({'username': current_user['name']})

    added_message = await UsersMessageDAO.add(**user_message)

    celery_app.send_task('calculate_text_lenght', (added_message.message, current_user["user_id"]))

    # await save_message_log(added_message.id)
    return {'status': 'ok'}


@router.get('/dashboard')
async def view_dashboard(current_user: dict = Depends(get_current_user)):
    username = current_user['name']
    user_id = current_user["user_id"]
    redis_tasks_info = get_tasks_count(user_id)

    rows = await UsersMessageDAO.find_with_limit(10, {"username": username})

    return {"redis": redis_tasks_info, "rows": rows}


async def save_message_log(message_id):
    await collection.insert_one({"saved_message_id": f"{message_id}", "status": "ok"})


def get_tasks_count(user_id: int | str) -> dict:
    # Получаем количество задач из Redis
    completed_tasks = redis_client.hget(user_id, "task")
    if completed_tasks is None:
        completed_tasks = 0  # Если данных нет, возвращаем 0

    return {"user_id": user_id, "completed_tasks": int(completed_tasks)}
