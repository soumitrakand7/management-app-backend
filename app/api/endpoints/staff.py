from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response, JSONResponse
from ...db.session import create_scheduler_log

from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps


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
    status = crud.staff_attendance.get_attendance_status(
        db=db, user_email=current_user)
    return {"attendance_status": status}
