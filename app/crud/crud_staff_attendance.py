from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models import StaffAttendance, StaffMember, StaffAbsence


class CRUDStaffAttendance(CRUDBase):
    def get(self, db: Session, user_email: str):
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.user_email == user_email).first()
        return staff_member_obj

    def check_in(self, db: Session, user_email: str):
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.user_email == user_email).first()
        staff_attendance_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == staff_member_obj.id).order_by(StaffAttendance.date.desc()).first()
        if staff_attendance.date == datetime.now().date:
            print(staff_attendance_obj.status)
        db_obj = StaffAttendance(
            staff_id=staff_member_obj.id,
            in_time=datetime.now().time(),
            date=datetime.now().date(),
            status='checked_in'
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def check_out(self, db: Session, user_email: str):
        staff_member_obj = self.get(db=db, user_email=user_email)
        staff_attendance_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == staff_member_obj.id).order_by(StaffAttendance.date.desc()).first()
        if datetime.now().date() != staff_attendance_obj.date:
            return False
        setattr(staff_attendance_obj, 'out_time',
                datetime.now().time())
        setattr(staff_attendance_obj, 'status', 'checked_out')
        db.add(staff_attendance_obj)
        db.commit()
        db.refresh(staff_attendance_obj)
        return staff_attendance_obj

    def get_absences(self, db: Session, user_email: str):
        staff_member_obj = self.get(db=db, user_email=user_email)
        member_absences = db.query(StaffAbsence.abscence_date).filter(
            StaffAbsence.staff_id == staff_member_obj.id).all()
        print(member_absences)
        return member_absences

    def get_attendance_status(self, db: Session, user_email: str):
        staff_member_obj = self.get(db=db, user_email=user_email)
        staff_attendance_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == staff_member_obj.id).order_by(StaffAttendance.date.desc()).first()
        if staff_attendance_obj is None or staff_attendance_obj.date != datetime.now().date():
            return 'absemt'
        return staff_attendance_obj.status


staff_attendance = CRUDStaffAttendance()
