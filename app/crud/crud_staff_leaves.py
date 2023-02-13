from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import StaffLeave
from app import crud
from backports.zoneinfo import ZoneInfo


from datetime import datetime, timedelta


class CRUDStaffLeaves(CRUDBase):
    def create(self, db: Session, leave_dict: Dict, user_email: str):
        staff_member_obj = crud.staff_management.get(
            db=db, user_email=user_email)
        starting_date = leave_dict.get('starting_date')
        ending_date = leave_dict.get('ending_date')
        starting_date_obj = datetime.strptime(starting_date, '%d/%m/%y')
        ending_date_obj = datetime.strptime(ending_date, '%d/%m/%y')
        staff_leave_obj = StaffLeave(
            staff_id=staff_member_obj.id,
            leave_subject=leave_dict.get('leave_subject'),
            reason=leave_dict.get('reason'),
            starting_date=starting_date_obj,
            ending_date=ending_date_obj,
            status='awaiting'
        )
        db.add(staff_leave_obj)
        db.commit()
        db.refresh(staff_leave_obj)
        return staff_leave_obj

    def is_on_leave(self, db: Session, staff_id: str) -> bool:
        staff_leave_obj = db.query(StaffLeave).filter(
            StaffLeave.staff_id == staff_id).order_by(StaffLeave.ending_date.desc()).first()
        if staff_leave_obj is None:
            return False
        return staff_leave_obj.ending_date > datetime.now(tz=ZoneInfo('Asia/Kolkata')).time() and staff_leave_obj.status == 'Approved'

    def get_application_status(self, db: Session, staff_id: str):
        staff_leave_obj = db.query(StaffLeave).filter(
            StaffLeave.staff_id == staff_id).order_by(StaffLeave.ending_date.desc()).first()
        return staff_leave_obj

    def update_leave_status(self, db: Session, staff_leave_id: str, status: str):
        staff_leave_obj = db.query(StaffLeave).filter(
            StaffLeave.id == staff_leave_id).first()
        setattr(staff_leave_obj, 'status', status)
        db.add(staff_leave_obj)
        db.commit()
        db.refresh(staff_leave_obj)
        return staff_leave_obj

    def get_leave_applications_by_staff(self, db: Session, staff_id: str):
        leave_applications = db.query(StaffLeave).filter(
            StaffLeave.staff_id == staff_id).all()
        return leave_applications

    def get_all_leave_applications(self, db: Session, subscriber_group_id: str):
        staff_members = crud.staff_management.get_members_by_subscriber_group(
            db=db, subscriber_group_id=subscriber_group_id)
        staff_leaves_list = []
        for member in staff_members:
            staff_details = crud.user.get_user_details(
                db=db, email=member.user_email)
            leave_applications = db.query(StaffLeave).filter(
                StaffLeave.staff_id == member.id).all()
            for appl in leave_applications:
                staff_leaves_list.append({
                    "leave_application": appl,
                    "staff_details": staff_details
                })

        return staff_leaves_list


staff_leave = CRUDStaffLeaves()
