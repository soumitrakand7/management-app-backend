from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


@router.post("/create-leave-application")
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    leave_application: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'staff':
        raise HTTPException(
            status_code=403,
            detail="Incorrect Profile",
        )
    response = crud.staff_leave.create(
        db=db, leave_dict=leave_application, user_email=current_user)
    return response


@router.put("/approve-application")
def approve_application(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    application_dict: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient Rights",
        )
    response = crud.staff_leave.update_leave_status(
        status='approved', db=db, staff_leave_id=application_dict.get('staff_leave_id'))
    return response


@router.put("/reject-application")
def reject_application(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    application_dict: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient Rights",
        )
    response = crud.staff_leave.update_leave_status(
        db=db, staff_leave_id=application_dict.get('staff_leave_id'), status='rejected')
    return response


@router.get("/get-leave-application-status")
def get_leave_application_status(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'staff':
        raise HTTPException(
            status_code=403,
            detail="Incorrect Profile",
        )
    staff_member_obj = crud.staff_management.get(
        db=db, user_email=current_user)
    application_obj = crud.staff_leave.get_application_status(
        db=db, staff_id=staff_member_obj.id)
    return application_obj


@router.get("/get-leave-applications-by-staff")
def get_leave_applications_by_staff(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'staff':
        raise HTTPException(
            status_code=403,
            detail="Incorrect Profile",
        )
    staff_member_obj = crud.staff_management.get(
        db=db, user_email=current_user)
    leave_applications = crud.staff_leave.get_leave_applications_by_staff(
        db=db, staff_id=staff_member_obj.id)
    return leave_applications


@router.get("/get-all-leave-applications")
def get_all_leave_applications(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient Rights",
        )
    staff_leaves_list = crud.staff_leave.get_all_leave_applications(
        db=db, subscriber_group_id=user_obj.subscriber_group_id)
    return staff_leaves_list
