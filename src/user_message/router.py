from fastapi import APIRouter, HTTPException, Response, status

from src.user_message.dao import UsersMessageDAO
from src.user_message.schemas import TestData

from src.storage import collection

router = APIRouter(prefix='/api', tags=['Api'])


@router.post('/submit')
async def get_json(data: TestData | None = None):
    user_message = data.dict()
    await UsersMessageDAO.add(**user_message)
    ins_id = (await collection.insert_one(user_message)).inserted_id
    print(f"Inserted_id id {ins_id}")
    return {'status': 'ok'}
