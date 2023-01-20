from typing import Dict
from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import Users, StaffMember, GuestMember, FamilyMember
from .base import CRUDBase
from ..models.user import Users
from integrations import mailer
import jinja2
from ..core.security import get_password_hash, verify_password

from app import crud

import string
import random


class CRUDProfile(CRUDBase):
    def create(self, db: Session, obj_in: Dict, admin_obj: Users):
        profile = obj_in.get('profile')
        subscriber_group_id = admin_obj.subscriber_group_id
        password = ''.join(random.choices(string.ascii_letters, k=7))

        db_obj = Users(
            email=obj_in.get("email"),
            hashed_password=get_password_hash(password),
            full_name=obj_in.get('full_name'),
            mobile_no=obj_in.get('mobile_no'),
            address=obj_in.get('address'),
            is_active=True,
            profile_image_url=obj_in.get('profile_image_url'),
            profile=profile,
            bank_ifsc=obj_in.get('bank_ifsc'),
            bank_account_no=obj_in.get('bank_account_no'),
            subscriber_group_id=subscriber_group_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        if profile == 'staff':
            staff_obj = StaffMember(
                user_email=db_obj.email,
                designation=obj_in.get('designation'),
                job_details=obj_in.get('job_details')
            )
            db.add(staff_obj)
            db.commit()
            db.refresh(staff_obj)

        elif profile == 'guest':
            guest_obj = GuestMember(
                user_email=db_obj.email,
                relation_tag=obj_in.get('relation_tag')
            )
            db.add(guest_obj)
            db.commit()
            db.refresh(guest_obj)

        elif profile == 'family':
            parent_email = ""
            child_email = ""
            relation_tag = obj_in.get('relation_tag')
            if relation_tag == 'Dad' or relation_tag == 'Mom':
                parent_email = obj_in.get('email')
                child_email = admin_obj.email
            elif relation_tag == 'Son' or relation_tag == 'Daughter':
                parent_email = admin_obj.email
                child_email = obj_in.get('email')
            family_member_obj = FamilyMember(
                parent_email=parent_email,
                child_email=child_email,
                subscriber_group_id=subscriber_group_id,
                relation_tag=obj_in.get('relation_tag')
            )
            db.add(family_member_obj)
            db.commit()
            db.refresh(family_member_obj)

        subscriber_group = db_obj.subscriber_group
        updated_member_count = subscriber_group.member_count + 1
        setattr(subscriber_group, 'member_count', updated_member_count)
        db.add(subscriber_group)
        db.commit()
        db.refresh(subscriber_group)

        crud.profile.send_activation_email(
            db=db, password=password, admin_obj=admin_obj, user_obj=db_obj)

        user_dict = db_obj.__dict__
        user_dict.pop('hashed_password')
        return user_dict

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
