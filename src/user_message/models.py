from sqlalchemy.orm import Mapped
from src.database import Base, int_pk, str_null_true


class UserMessage(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int]
    message: Mapped[str_null_true]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id!r},"
                f"message={self.message!r})")

    def __repr__(self):
        return str(self)
    