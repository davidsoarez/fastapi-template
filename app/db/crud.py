import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from app.db.sessions import Base
from typing import TypeVar
from sqlalchemy.sql.expression import column
from typing import List, Any

ModelType = TypeVar("ModelType", bound=Base)


class CrudBase:
    def __init__(self, model, soft_delete=False):
        self.model = model
        self.soft_delete = soft_delete

    def parse_query_params(self, query_params):

        params = []
        unused = []

        for key, value in query_params.items():
            if hasattr(self.model, key):

                if isinstance(query_params.get(key), List):
                    params.append(column(key).in_(value))

                else:
                    params.append(column(key) == value)
            else:
                unused.append(key)

        if unused:
            print(f'WARNING: "query_params" {unused} unused.')

        return params

    async def create(self, db: Session, obj: ModelType = None, value: dict = None, er=True):
        if value:
            obj = self.model(**value)
        try:
            async with db as conn:
                conn.add(obj)
                await conn.commit()

                return obj
        except Exception as error:
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    async def retrieve(self, db: Session, id: Any):

        query = select(self.model).where(self.model.id == id)

        try:
            async with db as conn:
                obj = await conn.execute(query)
                return obj.scalar()
        except Exception as error:
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    async def list(self, db: Session, params: dict = None):

        query_params = []

        query = select(self.model)

        if params:
            query_params += self.parse_query_params(query_params=params)
            query = select(self.model).where(*query_params)

        try:
            async with db as conn:
                obj = await conn.execute(query)
                return obj.scalars().all()
        except Exception as error:
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    async def update(self, db: Session, id: Any, values: dict):
        values['updated_at'] = datetime.now()

        query = update(self.model).where(self.model.id == id).values(values)

        try:
            async with db as conn:
                await conn.execute(query)
                await conn.commit()

                return True
        except Exception as error:
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    async def destroy(self, db: Session, id: Any):

        query = delete(self.model).where(self.model.id == id)

        try:
            async with db as conn:
                await conn.execute(query)
                await conn.commit()

                return True
        except Exception as error:
            raise HTTPException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)


