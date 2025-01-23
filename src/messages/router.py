from fastapi import APIRouter, Depends

from src.celery_app import calculate_text_lenght, get_tasks_count

from src.storage import save_message_log
from src.users.router import get_current_user
from src.messages.schemas import TestData
from src.messages.dao import MessageDAO
from src.users.dao import UserDAO


router = APIRouter(prefix='/api/message', tags=['ApiMessage'])


@router.post('/submit')
async def get_json(data: TestData | None = None, current_user: dict = Depends(get_current_user)) -> dict:
    user_message = data.dict()
    user_message.update({'username': current_user['username'], 'user_id': int(current_user['user_id'])})
    added_message = await MessageDAO.add(**user_message)

    calculate_text_lenght.apply_async(args=[added_message.message, current_user["user_id"]])

    await save_message_log(added_message.id)
    return {'message': 'Your message saved!'}


@router.get('/dashboard')
async def view_dashboard(current_user: dict = Depends(get_current_user)):
    username = current_user['username']
    user_id = current_user["user_id"]
    redis_tasks_info = get_tasks_count(user_id)

    # rows = await MessageDAO.find_all()
    rows = await MessageDAO.find_with_limit(10, {"username": username})


    return {"tasks": redis_tasks_info, "rows": rows}
