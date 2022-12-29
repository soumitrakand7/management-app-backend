from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from ..core.security import get_password_hash, verify_password

from .base import CRUDBase
from ..models.user import Users


class CRUDUser(CRUDBase):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def create(self, db: Session, *, obj_in: Dict) -> Users:
        db_obj = Users(
            email=obj_in.get("email"),
            hashed_password=get_password_hash(obj_in.get("password")),
            first_name=obj_in.get("first_name"),
            last_name=obj_in.get("last_name"),
            mobile_no=obj_in.get('mobile_no'),
            address=obj_in.get('address'),
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_users(self, db: Session):
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

    def get_user_details(self, db: Session, email: str):
        user_obj = db.query(Users).filter(Users.email == email).first()
        user_dict = user_obj.__dict__
        user_dict.pop('hashed_password')
        return user_dict


user = CRUDUser()


# {
#     "email": "soumitrakand3@gmail.com",
#     "first_name": "Soumitra",
#     "last_name": "kand",
#     "mobile_no": "9822571054",
#     "address": "Warje, Pune",
#     "password": "1234"
# }
