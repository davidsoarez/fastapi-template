from fastapi import APIRouter
from app.users.view import users

urls = APIRouter()

urls.include_router(users, tags=["users"])
