from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse

from src.user_message.dao import UsersMessageDAO
from src.user_message.schemas import TestData, OutTasksInfo

from src.storage import collection

from src.celery_app import app as celery_app

router = APIRouter(prefix='/api', tags=['Api'])


@router.post('/submit')
async def get_json(data: TestData | None = None):
    user_message = data.dict()
    added_message = await UsersMessageDAO.add(**user_message)
    await save_message_log(added_message.id)

    celery_app.send_task('calculate_text_lenght', (added_message.message,))
    return {'status': 'ok'}


@router.get('/dashboard')
async def view_dashboard():
    redis_tasks_count = get_tasks_count(celery_app)
    rows = await UsersMessageDAO.find_with_limit(10)

    return {'done_tasks_count': redis_tasks_count, 'info': rows}


async def save_message_log(message_id):
    await collection.insert_one({"saved_message_id": f"{message_id}", "status": "ok"})


def get_tasks_count(c_app):
    tasks_count = 0
    inspect = c_app.control.inspect()
    stats = inspect.stats()

    for worker, stat in stats.items():
        tasks_count = stat['total']['calculate_text_lenght']

    return tasks_count
