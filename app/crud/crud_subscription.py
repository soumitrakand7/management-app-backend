from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from app import crud

from app.crud.base import CRUDBase
from app.models import SubscriptionPlan, Users


class CRUDSubscriptions(CRUDBase):
    def create(self, db: Session, sub_plan_dict: Dict):
        sub_plan_obj = SubscriptionPlan(
            min_members=sub_plan_dict.get('min_members'),
            max_members=sub_plan_dict.get('max_members'),
            plan_name=sub_plan_dict.get('plan_name'),
            price=sub_plan_dict.get('price')
        )
        db.add(sub_plan_obj)
        db.commit()
        db.refresh(sub_plan_obj)
        return sub_plan_obj

    def get(self, db: Session, plan_id: str):
        sub_plan = db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id).first()
        return sub_plan

    def get_all_plans(self, db: Session):
        sub_plans = db.query(SubscriptionPlan).all()
        for plan in sub_plans:
            print(plan.user.email)
        return sub_plans

    def set_user_plan(self, db: Session, user_email: str, plan_id: str) -> Users:
        user_obj = crud.user.get_by_email(db=db, email=user_email)
        setattr(user_obj, 'plan_id', plan_id)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


sub_plan = CRUDSubscriptions()
