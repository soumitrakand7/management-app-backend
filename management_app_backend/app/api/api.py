from fastapi import APIRouter

from .endpoints import (users, login, subscription_plan)

api_router = APIRouter()


api_router.include_router(users.router, prefix="/user", tags=["register-user"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    subscription_plan.router, prefix="/subscriptions", tags=["subscription-plan"])
