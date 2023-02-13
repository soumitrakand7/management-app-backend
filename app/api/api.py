from fastapi import APIRouter

from .endpoints import (staff_attendance, users, login, subscription_plan,
                        subscriber, profiles, satff_tasks, staff_leaves, chats)

api_router = APIRouter()


api_router.include_router(users.router, prefix="/user", tags=["register-user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(
    subscription_plan.router, prefix="/subscriptions", tags=["subscription-plan"])
api_router.include_router(
    subscriber.router, prefix="/subscriber", tags=["subscriber"])
api_router.include_router(
    profiles.router, prefix="/profile", tags=["profiles"])
api_router.include_router(
    staff_attendance.router, prefix="/staff-attendance", tags=["staff-attendance"])
api_router.include_router(
    satff_tasks.router, prefix="/staff-task", tags=["staff-task"])
api_router.include_router(
    staff_leaves.router, prefix="/staff-leave", tags=["staff-leave"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
