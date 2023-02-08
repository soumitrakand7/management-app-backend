from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response, JSONResponse

from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


@router.post("/create")
def create_profile(
    *,
    db: Session = Depends(deps.get_db),
    user_in: Dict,
    current_user: models.Users = Depends(deps.get_current_user)
) -> Any:
    """
    Create new profile.
    """
    user = crud.user.get_by_email(db, email=user_in.get("email"))
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_obj = crud.user.get_by_email(db=db, email=current_user)

    if not crud.sub_plan.is_group_available(db=db, subscriber_group_id=user_obj.subscriber_group_id):
        raise HTTPException(
            status_code=400,
            detail="Subscription group full",
        )
    success = crud.profile.create(db=db, obj_in=user_in, admin_obj=user_obj)
    return success


@router.get("/get-family-tree")
def get_family_tree(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    family_tree = crud.profile.get_family_tree(
        db=db, subscriber_group_id=user_obj.subscriber_group_id)
    print(user_obj.full_name)
    print(user_obj.subscriber_group_id)
    return family_tree


@router.get("/get-staff-members")
def get_staff_members(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    # if user_obj.profile != 'admin':
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Insufficient Rights",
    #     )
    staff_members = crud.staff_management.get_members_by_subscriber_group(
        db=db, subscriber_group_id=user_obj.subscriber_group_id)
    members_list = []
    for member in staff_members:
        member_dict = member.__dict__
        user_details = crud.user.get_user_details(
            db=db, email=member.user_email)
        member_dict['profile_image_url'] = user_details.get(
            'profile_image_url')
        member_dict['full_name'] = user_details.get('full_name')
        members_list.append(member_dict)
    return members_list


@router.get("/get-staff-tree")
def get_staff_tree(
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    staff_tree = crud.staff_tree.get_staff_tree(
        db=db, subscriber_group_id=user_obj.subscriber_group_id)
    print(user_obj.full_name)
    print(user_obj.subscriber_group_id)
    return staff_tree


@router.put("/update-node")
def update_node(
    node_dict: Dict,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    member_email = node_dict.get('member_email')
    member_obj = crud.user.get_by_email(db=db, email=member_email)
    parent_obj = crud.user.get_by_email(
        db=db, email=node_dict.get('parent_email'))
    if crud.user.is_admin(db=db, user_email=current_user):
        result = crud.profile.update_parent(
            db=db, parent_obj=parent_obj, user_obj=member_obj, node_id=node_dict.get('id'))
        if not result:
            raise HTTPException(
                status_code=403, detail="Incorrect email or subscriber id")
        return JSONResponse({"success": 1})
    else:
        raise HTTPException(
            status_code=401, detail="Insufficient rights")
