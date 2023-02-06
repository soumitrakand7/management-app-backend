from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps
from ...core.s3_image_upload import upload_to_s3_bucket
import uuid

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


@router.post("/upload-profile-image")
def upload_profile_image(
    db: Session = Depends(deps.get_db),
    *,
    current_user: str = Depends(deps.get_current_user),
    profile_image_details: Dict
):
    image = profile_image_details.get('profile_image')
    user_obj = crud.user.get_by_email(db=db, email=current_user)

    s3_file_name = user_obj.full_name.lower() + '-' + str(uuid.uuid4()) + \
        '-profile-image'
    s3_file_name = s3_file_name.replace('#', '-')
    profile_image_url = upload_to_s3_bucket(
        image,
        'management-app-user-profile-images',
        s3_file_name.replace(" ", "-")
    )
    setattr(user_obj, 'profile_image_url', profile_image_url)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"profile_image_url": profile_image_url}
