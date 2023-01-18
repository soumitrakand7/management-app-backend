from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import Users, StaffMember, GuestMember, FamilyMember
from .base import CRUDBase
from ..models.user import Users
from integrations import mailer
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
                parent_email=profile_dict.get('parent_email'),
                child_email=user_obj.email,
                subscriber_group_id=user_obj.subscriber_group_id
            )
            db.add(family_member_obj)
            db.commit()
            db.refresh(family_member_obj)

        subscriber_group = user_obj.subscriber_group
        admin_obj = subscriber_group.admin
        print(admin_obj.full_name)
        updated_member_count = subscriber_group.member_count + 1
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
        response = mailer.send_email(
            receiver_email=user_obj.email, subject="Activation of Account", email_content=registration_template)
        print(response)
        return response

    def get_family_tree(self, db: Session, subscriber_group_id: str):
        family_relations = db.query(FamilyMember).filter(
            FamilyMember.subscriber_group_id == subscriber_group_id).all()
        member_emails = set()
        for member in family_relations:
            member_emails.add(member.child_email)
            member_emails.add(member.parent_email)
        member_emails.discard(None)
        users_list = []
        for email in member_emails:
            users_list.append(crud.user.get_user_details(db=db, email=email))
        return {"user_realtions": family_relations, "users": users_list}

    def update_node(self, db: Session, user_email: str, node_id: str, fields: Dict):
        node_obj = db.query(FamilyMember).filter(
            FamilyMember.child_email == user_email).filter(FamilyMember.id == node_id).first()
        super().update(db=db, db_obj=node_obj, obj_in=fields)
        return node_obj

    def update_parent(self, db: Session, user_obj: Users, node_id: str, parent_obj: Users):
        node_obj = db.query(FamilyMember).filter(
            FamilyMember.child_email == user_obj.email).filter(FamilyMember.id == node_id).first()
        print(parent_obj)
        print(node_obj)
        success = parent_obj is not None and node_obj.subscriber_group_id == parent_obj.subscriber_group_id
        if success:
            setattr(node_obj, 'parent_email', parent_obj.email)
            db.add(node_obj)
            db.commit()
            db.refresh(node_obj)
        return success


profile = CRUDProfile()
