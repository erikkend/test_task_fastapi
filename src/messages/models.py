from sqlalchemy.orm import Mapped
from src.database import Base, int_pk, str_null_true, str_uniq


class Message(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int]
    username: Mapped[str_uniq]
    message: Mapped[str_null_true]

    def __repr__(self):
        return ("{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id!r},"
                f"username={self.username!r},"
                f"message={self.message!r})")