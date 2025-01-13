from src.dao.base import BaseDAO
from src.user_message.models import UserMessage


class UsersMessageDAO(BaseDAO):
    model = UserMessage
