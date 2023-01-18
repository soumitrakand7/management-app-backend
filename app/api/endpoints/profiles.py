from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response, JSONResponse

from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


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
