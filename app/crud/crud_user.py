from typing import Dict, Optional, Any, List
from sqlalchemy.orm import Session
from ..core.security import get_password_hash, verify_password
import random
from .base import CRUDBase
from ..models.user import Users
from integrations import mailer
from datetime import datetime
from app import crud
import jinja2

import string
import random


class CRUDUser(CRUDBase):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def create(self, db: Session, *, obj_in: Dict) -> Any:
        profile = obj_in.get('profile')
        subscriber_group_id = obj_in.get('subscriber_group_id')

        if profile != 'admin' and not crud.sub_plan.is_group_available(db=db, subscriber_group_id=subscriber_group_id):
            return False

        password = obj_in.get("password") if profile == 'admin' else ''.join(
            random.choices(string.ascii_letters, k=7))
        db_obj = Users(
            email=obj_in.get("email"),
            hashed_password=get_password_hash(password),
            full_name=obj_in.get('full_name'),
            mobile_no=obj_in.get('mobile_no'),
            address=obj_in.get('address'),
            is_active=False,
            profile_image_url=obj_in.get('profile_image_url'),
            profile=obj_in.get('profile')
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        if profile != 'admin':
            if not crud.sub_plan.get_subscriber_group(db=db, subscriber_group_id=subscriber_group_id):
                return False
            setattr(db_obj, 'subscriber_group_id', subscriber_group_id)
            setattr(db_obj, 'is_active', True)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            crud.profile.create_profile(
                db=db, user_obj=db_obj, profile_dict=obj_in, profile=profile, password=password)

        else:
            crud.user.send_verification_otp(db=db, user_obj=db_obj)

        user_dict = db_obj.__dict__
        user_dict.pop('hashed_password')
        return user_dict

    def get_users(self, db: Session) -> List[Users]:
        db_users = db.query(Users).all()
        return db_users

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Users]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Users) -> bool:
        return user.is_active

    def update(self, db: Session, *, db_obj: Users, obj_in: Dict[str, Any]) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        if update_data.get("password", None):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_user_details(self, db: Session, email: str) -> Dict[str, Any]:
        user_obj = crud.user.get_by_email(db=db, email=email)
        user_dict = user_obj.__dict__
        print(user_obj.plan.plan_name)
        user_dict.pop('hashed_password')
        return user_dict

    def activate_user(self, db: Session, user_obj: Users, activation_code: int) -> bool:
        minutes = divmod(
            (datetime.now() - user_obj.registration_date).total_seconds(), 60)[0]
        success = user_obj.activation_code == activation_code and minutes < 5
        if success:
            setattr(user_obj, 'is_active', True)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
        return success

    def send_verification_otp(self, db: Session, user_obj: Users) -> Users:
        activation_code = random.randint(1000, 9999)
        with open("templates/registration-successful.html", "r") as f:
            template_string = f.read()
        template = jinja2.Template(template_string)
        registration_template = template.render(
            activation_code=activation_code, full_name=user_obj.full_name)
        response = mailer.send_email(
            receiver_email=user_obj.email, subject="OTP for Login", email_content=registration_template)
        print(response)
        setattr(user_obj, 'activation_code', activation_code)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


user = CRUDUser()
