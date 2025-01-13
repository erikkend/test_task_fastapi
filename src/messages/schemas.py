from pydantic import BaseModel


class TestData(BaseModel):
    user_id: int
    username: str
    message: str | None
