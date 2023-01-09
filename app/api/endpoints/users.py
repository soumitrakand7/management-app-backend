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


@router.put("/set-plan")
def set_subscription_plan(
    plan_dict: Dict,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    plan_id = plan_dict.get('plan_id')
    plan_obj = crud.sub_plan.get(db=db, plan_id=plan_id)
    if not plan_obj:
        raise HTTPException(
            status_code=404,
            detail="Invalid id or plan does not exist"
        )
    updated_user_obj = crud.sub_plan.set_user_plan(
        db=db, plan_id=plan_id, user_email=current_user)
    return updated_user_obj
