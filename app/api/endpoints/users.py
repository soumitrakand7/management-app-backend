from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


@router.post("/register")
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: Dict,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.get("email"))
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    success = crud.user.create(db, obj_in=user_in)
    return success


@router.get("/get-user-details")
def get_users(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
) -> List:
    user_details = crud.user.get_user_details(db=db, email=current_user)

    return user_details
