from fastapi import APIRouter

from .endpoints import (users, login)

api_router = APIRouter()


api_router.include_router(users.router, prefix="/user", tags=["register-user"])
api_router.include_router(login.router, tags=["login"])
