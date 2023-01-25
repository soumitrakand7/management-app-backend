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
