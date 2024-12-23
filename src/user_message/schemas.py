from pydantic import BaseModel


class TestData(BaseModel):
    user_id: int
    message: str | None
