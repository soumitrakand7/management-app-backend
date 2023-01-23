from fastapi import APIRouter

from .endpoints import (users, login, subscription_plan,
                        subscriber, profiles, staff)

api_router = APIRouter()


api_router.include_router(users.router, prefix="/user", tags=["register-user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(
    subscription_plan.router, prefix="/subscriptions", tags=["subscription-plan"])
api_router.include_router(
    subscriber.router, prefix="/subscriber", tags=["subscriber"])
api_router.include_router(
    profiles.router, prefix="/profile", tags=["profiles"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
