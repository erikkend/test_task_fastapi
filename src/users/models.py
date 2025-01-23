from sqlalchemy.orm import Mapped
from src.database import Base, int_pk, str_uniq


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]

    def __str__(self):
        return (f"{self.__class__.__name__}(user_id={self.id}, "
                f"username={self.username!r},")

    def __repr__(self):
        return str(self)