from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.database import Session


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with Session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_with_limit(cls, limit_number: int, filter_by: dict):
        async with Session() as session:
            query = select(cls.model).filter_by(**filter_by).order_by(cls.model.id.desc()).limit(limit_number)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with Session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
