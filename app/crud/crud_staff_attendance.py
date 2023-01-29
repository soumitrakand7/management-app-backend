from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime
from backports.zoneinfo import ZoneInfo

from app.crud.base import CRUDBase
from app.models import StaffAttendance, StaffMember, StaffAbsence


class CRUDStaffAttendance(CRUDBase):
    def get(self, db: Session, user_email: str) -> StaffMember:
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.user_email == user_email).first()
        return staff_member_obj

    def check_in(self, db: Session, user_email: str):
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.user_email == user_email).first()
        
        staff_attendance_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == staff_member_obj.id).order_by(StaffAttendance.date.desc()).first()

        # print(staff_attendance_obj.date)
        # print(datetime.now(tz=ZoneInfo('Asia/Kolkata')).date())
        if staff_attendance_obj is None:
            db_obj = StaffAttendance(
                staff_id=staff_member_obj.id,
                check_in_time=datetime.now(tz=ZoneInfo('Asia/Kolkata')).time(),
                date=datetime.now(tz=ZoneInfo('Asia/Kolkata')).date(),
                status='checked_in'
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        elif staff_attendance_obj.date != datetime.now(tz=ZoneInfo('Asia/Kolkata')).date():
            print("HERE")
            db_obj = StaffAttendance(
                staff_id=staff_member_obj.id,
                check_in_time=datetime.now(tz=ZoneInfo('Asia/Kolkata')).time(),
                date=datetime.now(tz=ZoneInfo('Asia/Kolkata')).date(),
                status='checked_in'
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        elif staff_attendance_obj.date == datetime.now(tz=ZoneInfo('Asia/Kolkata')).date():
            setattr(staff_attendance_obj, 'check_in_time',
                    datetime.now(tz=ZoneInfo('Asia/Kolkata')).time())
            db.add(staff_attendance_obj)
            db.commit()
            db.refresh(staff_attendance_obj)
            # print(staff_attendance_obj)
            return staff_attendance_obj

    def check_out(self, db: Session, user_email: str):
        staff_member_obj = self.get(db=db, user_email=user_email)
        staff_attendance_obj = db.query(StaffAttendance).filter(
            StaffAttendance.staff_id == staff_member_obj.id).order_by(StaffAttendance.date.desc()).first()
        if datetime.now(tz=ZoneInfo('Asia/Kolkata')).date() != staff_attendance_obj.date:
            return False
        setattr(staff_attendance_obj, 'check_out_time',
                datetime.now(tz=ZoneInfo('Asia/Kolkata')).time())
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
        print(staff_attendance_obj)
        if staff_attendance_obj is None or staff_attendance_obj.date != datetime.now(tz=ZoneInfo('Asia/Kolkata')).date():
            return {
                "status": 'absent',
                "check_in_time": None,
                "check_out_time": None
            }

        return {
            "status": staff_attendance_obj.status,
            "check_in_time": staff_attendance_obj.check_in_time,
            "check_out_time": staff_attendance_obj.check_out_time
        }


staff_attendance = CRUDStaffAttendance()
