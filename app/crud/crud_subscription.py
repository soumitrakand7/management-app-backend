from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from app import crud

from app.crud.base import CRUDBase
from app.models import SubscriptionPlan, Users, SubscriberGroup


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

    def create_subscription_group(self, db: Session, admin_user_obj: Users):
        # admin_profile = crud.user

        pass

    def get_subscriber_group(self, db: Session, subscriber_group_id: str):
        return db.query(SubscriberGroup).get(id=subscriber_group_id)


sub_plan = CRUDSubscriptions()
