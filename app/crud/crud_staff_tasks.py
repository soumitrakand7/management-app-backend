from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import StaffTask
from .base import CRUDBase
from app import crud

from datetime import datetime


class CRUDStaffTasks(CRUDBase):
    def create(self, db: Session, user_email: str, obj_in: Dict):
        staff_member_obj = crud.staff_attendance.get(
            db=db, user_email=user_email)
        staff_task_obj = StaffTask(
            staff_id=staff_member_obj.id,
            task_title=obj_in.get('task_title'),
            description=obj_in.get('description'),
            assigned_at=datetime.now(),
            valid_for=obj_in.get('valid_for')
        )
        db.add(staff_task_obj)
        db.commit()
        db.refresh(staff_task_obj)
        return staff_task_obj

    def get_all_tasks(self, db: Session, user_email: str):
        staff_member_obj = crud.staff_attendance.get(
            db=db, user_email=user_email)
        tasks = db.query(StaffTask).filter(
            StaffTask.staff_id == staff_member_obj.id).order_by(StaffTask.assigned_at)
        return tasks


staff_tasks = CRUDStaffTasks()
