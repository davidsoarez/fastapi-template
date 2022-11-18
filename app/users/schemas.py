
from pydantic import BaseModel, UUID4


class UserCreate(BaseModel):
    first_name: str
    last_name: str


class UserList(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserRetrieve(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
