from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DB_ASYNC_CONN: str = 'postgresql+asyncpg://postgres:secret@srvdb-template/template'
    DB_POOL_SIZE: int = 5


settings = Settings()
