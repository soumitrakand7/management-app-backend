from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


@router.post("/create")
def create_subscriber_group(
    plan_dict: Dict,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
) -> Any:
    plan_id = plan_dict.get('plan_id')
    plan_obj = crud.sub_plan.get(db=db, plan_id=plan_id)
    admin_profile = crud.user.get_by_email(db=db, email=current_user)
    if admin_profile.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient rights to subscribe to a plan",
        )
    if not plan_obj:
        raise HTTPException(
            status_code=404,
            detail="Invalid id or plan does not exist"
        )
    updated_user_obj = crud.sub_plan.create_subscription_group(
        db=db, subscription_plan_obj=plan_obj, admin_profile=admin_profile)
    return updated_user_obj


@router.get("/get")
def get_subscriber_group(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
):
    subscriber_group = crud.sub_plan.get_subscriber_group_by_user(
        db=db, user_email=current_user)
    return subscriber_group


@router.get("/get-members")
def get_members(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
):
    group_members = crud.sub_plan.get_group_users(
        db=db, user_email=current_user)
    return group_members
