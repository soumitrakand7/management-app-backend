from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response, JSONResponse
from ...db.session import create_scheduler_log

from sqlalchemy.orm import Session
from ... import crud, models
from ...models import StaffMember, StaffAttendance, StaffAbsence
from .. import deps

from datetime import datetime


router = APIRouter()


@router.post("/check-in")
def check_in(
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
    response = crud.staff_attendance.check_in(
        db=db, user_email=current_user)
    print(response)
    return response


@router.post("/check-out")
def check_out(
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
    response = crud.staff_attendance.check_out(
        db=db, user_email=current_user)
    return response


@router.get("/get-attendance-status")
def get_attendance_status(
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
    attendance = crud.staff_attendance.get_attendance_status(
        db=db, user_email=current_user)
    return attendance


@router.get("/get-absences")
def get_attendance_status(
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
    absences = crud.staff_attendance.get_absences(
        db=db, user_email=current_user)
    return absences


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
    response = crud.staff_leave.approve_application(
        db=db, staff_leave_id=application_dict.get('staff_leave_id'))
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
    staff_member_obj = crud.staff_attendance.get(
        db=db, user_email=current_user)
    application_status = crud.staff_leave.get_application_status(
        db=db, staff_id=staff_member_obj.id)
    return {"application_status": application_status}


@create_scheduler_log(job_name="Check Abscences")
def check_abscences(
    *,
    db: Session = Depends(deps.get_db),
):
    print("HERE ###")
    staff_members = db.query(StaffMember).filter(
        StaffMember.employment_status == 'employed').all()
    for member in staff_members:
        staff_att_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == member.id).order_by(StaffAttendance.date.desc()).first()
        if staff_att_obj.date != datetime.now().date:
            staff_absence_obj = StaffAbsence(
                staff_id=member.id,
                abscence_date=datetime.now().date
            )
            db.add(staff_absence_obj)
            db.commit()
            db.refresh(staff_absence_obj)
