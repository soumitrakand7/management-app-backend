from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from ..core.security import get_password_hash, verify_password
import random
from .base import CRUDBase
from app.models import Users, StaffMember, GuestMember, FamilyMember
from integrations import auth_mailer
from datetime import datetime
from app import crud
import jinja2


class CRUDProfile(CRUDBase):
    def create_profile(self, db: Session, user_obj: Users, profile: str, profile_dict: Dict):
        if profile == 'staff':
            staff_obj = StaffMember(
                user_email=user_obj.email,
                designation=profile_dict.get('designation'),
                job_details=profile_dict.get('job_details')
            )
            db.add(staff_obj)
            db.commit()
            db.refresh(staff_obj)
        elif profile == 'guest':
            guest_obj = GuestMember(
                user_email=user_obj.email,
                relation_tag=profile_dict.get('relation_tag')
            )
            db.add(guest_obj)
            db.commit()
            db.refresh(guest_obj)
        elif profile == 'family':
            family_member_obj = FamilyMember(
                relation_tag=profile_dict.get('relation_tag'),
                user_email=user_obj.email
            )
            db.add(family_member_obj)
            db.commit()
            db.refresh()


profile = CRUDProfile()
