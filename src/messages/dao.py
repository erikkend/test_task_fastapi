from src.dao.base import BaseDAO
from src.messages.models import Message


class MessageDAO(BaseDAO):
    model = Message
