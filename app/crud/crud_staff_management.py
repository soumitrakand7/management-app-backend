from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from datetime import datetime
from backports.zoneinfo import ZoneInfo

from app.crud.base import CRUDBase
from app.models import StaffAttendance, StaffMember, Users


class CRUDStaffManagement(CRUDBase):
    def get(self, db: Session, user_email: str) -> StaffMember:
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.user_email == user_email).first()
        return staff_member_obj

    def get_by_id(self, db: Session, staff_member_id: str) -> StaffMember:
        staff_member_obj = db.query(StaffMember).filter(
            StaffMember.id == staff_member_id).first()
        return staff_member_obj

    def get_members_by_subscriber_group(self, db: Session, subscriber_group_id):
        staff_members = db.query(StaffMember).join(Users).filter(
            Users.subscriber_group_id == subscriber_group_id).filter(Users.profile == 'staff').all()
        return staff_members


staff_management = CRUDStaffManagement()
