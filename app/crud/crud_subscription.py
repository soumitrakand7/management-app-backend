from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from app import crud
from datetime import datetime

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
            print(plan)
        return sub_plans

    def create_subscription_group(self, db: Session, admin_profile: Users, subscription_plan_obj: SubscriptionPlan) -> Any:
        print(admin_profile.email)
        print(subscription_plan_obj.id)
        subscriber_grp_obj = SubscriberGroup(
            admin_email=admin_profile.email,
            plan_id=subscription_plan_obj.id,
            valid_until=datetime.max,
            member_count=1
        )
        db.add(subscriber_grp_obj)
        db.commit()
        db.refresh(subscriber_grp_obj)
        return subscriber_grp_obj

    def get_subscriber_group(self, db: Session, subscriber_group_id: str):
        return db.query(SubscriberGroup).filter(SubscriberGroup.id == subscriber_group_id).first()

    def get_subscriber_group_by_user(self, db: Session, user_email: str):
        user_obj = crud.user.get_by_email(db=db, email=user_email)
        return user_obj.subscriber_group

    def is_group_available(self, db: Session, subscriber_group_id: str):
        subscriber_group_obj = self.get_subscriber_group(
            db=db, subscriber_group_id=subscriber_group_id)
        return subscriber_group_obj.member_count < subscriber_group_obj.subscription_plan.max_members


sub_plan = CRUDSubscriptions()
