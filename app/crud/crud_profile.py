from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import Users, StaffMember, GuestMember, FamilyMember
from .base import CRUDBase
from ..models.user import Users
from integrations import auth_mailer
import jinja2
from app import crud


class CRUDProfile(CRUDBase):
    def create_profile(self, db: Session, user_obj: Users, profile: str, profile_dict: Dict, password: str):
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
            db.refresh(family_member_obj)

        subscriber_group = user_obj.subscriber_group
        admin_obj = subscriber_group.admin
        print(admin_obj.full_name)
        updated_member_count += subscriber_group.member_count
        setattr(subscriber_group, 'member_count', updated_member_count)
        db.add(subscriber_group)
        db.commit()
        db.refresh(subscriber_group)

        crud.profile.send_activation_email(
            db=db, password=password, admin_obj=admin_obj, user_obj=user_obj)
        return True

    def send_activation_email(self, db: Session, admin_obj: Users, user_obj: Users, password: str):
        with open("templates/invite-member.html", "r") as f:
            template_string = f.read()
        template = jinja2.Template(template_string)
        registration_template = template.render(
            user_name=user_obj.full_name,
            admin_name=admin_obj.full_name,
            profile_email=user_obj.email,
            password=password
        )
        response = auth_mailer.send_email(
            receiver_email=user_obj.email, subject="Activation of Account", email_content=registration_template)
        print(response)
        return response


profile = CRUDProfile()
