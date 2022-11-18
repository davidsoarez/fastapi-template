from fastapi import APIRouter, Request, Depends, status, Response
from app.users.schemas import *
from app.users.crud import *
from sqlalchemy.orm import Session
from ..db.sessions import get_db


users = APIRouter()


@users.post('/account', status_code=status.HTTP_201_CREATED)
async def create(request: Request, body: UserCreate, db: Session = Depends(get_db)):
    body = body.dict()
    response = await user.create(db=db, value=body)

    return {"message": "successfully"}


@users.get("/account", status_code=status.HTTP_200_OK)
async def list(request: Request, db: Session = Depends(get_db)):

    response = await user.list(db=db)
    if not response:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    response = [UserList.from_orm(obj) for obj in response]

    return response


@users.get("/account/{id}", status_code=status.HTTP_200_OK, response_model=UserRetrieve)
async def retrieve(request: Request, id: int, db: Session = Depends(get_db)):

    response = await user.retrieve(db=db, id=id)
    if not response:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return response
