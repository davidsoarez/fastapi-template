from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base


class DbConnect:
    def __init__(self, url_async=None):
        self.url_async = url_async

        self.engine = create_async_engine(self.url_async, pool_size=settings.DB_POOL_SIZE)
        self.session_local = sessionmaker(bind=self.engine, autoflush=False,
                                            autocommit=False, expire_on_commit=False,
                                            class_=AsyncSession)


db = DbConnect(url_async=settings.DB_ASYNC_CONN)

Base = declarative_base()


def get_db():
    try:
        yield db.session_local()
    finally:
        pass
