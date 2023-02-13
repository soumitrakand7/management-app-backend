from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


router = APIRouter()


@router.post("/create-task")
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    task_dict: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient Rights",
        )
    task_obj = crud.staff_tasks.create(
        db=db, obj_in=task_dict, subscriber_group_id=user_obj.subscriber_group_id)
    return task_obj


@router.get("/get-tasks-by-staff")
def get_tasks(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
):
    staff_tasks = crud.staff_tasks.get_all_tasks(
        db=db, user_email=current_user)
    return staff_tasks


@router.get("/get-tasks-by-group")
def get_tasks_by_subscriber_group(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user)
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    tasks = crud.staff_tasks.get_tasks_by_subscriber_grp(
        db=db, subscriber_grp=user_obj.subscriber_group)
    return tasks


@router.put("/update-task")
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    task_details: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Insufficient Rights",
        )
    updated_task = crud.staff_tasks.update_task(
        db=db, fields=task_details, task_id=task_details.get('task_id'))
    return updated_task


@router.put("/update-task-by-staff")
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.Users = Depends(deps.get_current_user),
    task_details: Dict
):
    user_obj = crud.user.get_by_email(db=db, email=current_user)
    if user_obj.profile != 'staff':
        raise HTTPException(
            status_code=403,
            detail="Incorrect Profile",
        )
    updated_task = crud.staff_tasks.update_status(
        db=db, status=task_details.get('status'), task_id=task_details.get('task_id'))
    return updated_task
