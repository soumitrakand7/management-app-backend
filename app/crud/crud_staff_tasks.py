from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import StaffTask, StaffTaskMapping
from .base import CRUDBase
from app import crud

from datetime import datetime, timedelta


class CRUDStaffTasks(CRUDBase):
    def create(self, db: Session,  obj_in: Dict):
        valid_from = obj_in.get('valid_from')
        datetime_object = datetime.strptime(valid_from, '%d/%m/%y %H:%M')
        staff_emails = obj_in.get('staff_emails')
        staff_task_obj = StaffTask(
            task_title=obj_in.get('task_title'),
            description=obj_in.get('description'),
            assigned_at=datetime.now(),
            priority=obj_in.get('priority'),
            valid_from=datetime_object,
            status='Active',
            valid_for=obj_in.get('valid_for')
        )
        db.add(staff_task_obj)
        db.commit()
        db.refresh(staff_task_obj)

        for member_email in staff_emails:
            staff_member_obj = crud.staff_attendance.get(
                db=db, user_email=member_email)
            db_obj = StaffTaskMapping(
                task_id=staff_task_obj.id,
                staff_id=staff_member_obj.id
            )
            db.add(db_obj)
            db.commit()

        return staff_task_obj

    def get_all_tasks(self, db: Session, user_email: str):
        staff_member_obj = crud.staff_attendance.get(
            db=db, user_email=user_email)
        staff_task_mapped_objs = db.query(StaffTaskMapping).filter(
            StaffTaskMapping.staff_id == staff_member_obj.id).all()
        active_tasks = []
        for obj in staff_task_mapped_objs:
            task_id = obj.task_id
            staff_task_obj = db.query(StaffTask).filter(
                StaffTask.id == task_id).first()
            if self.is_active_task(task_obj=staff_task_obj):
                active_tasks.append(staff_task_obj)
        return active_tasks

    def update_status(self, db: Session, task_id: str, status: str):
        task_obj = db.query(StaffTask).filter(StaffTask.id == task_id).first()
        setattr(task_obj, 'status', status)
        db.add(task_obj)
        db.commit()
        db.refresh(task_obj)
        return task_obj

    def is_active_task(self, task_obj: StaffTask):
        return task_obj.valid_from + timedelta(hours=task_obj.valid_for) < datetime.now() and task_obj.status == 'Active'


staff_tasks = CRUDStaffTasks()
