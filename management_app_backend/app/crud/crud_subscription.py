from typing import Dict, Optional, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import SubscriptionPlan


class CRUDSubscriptions(CRUDBase):
    def create(self, db: Session, sub_plan_dict: Dict):
        sub_plan_obj = SubscriptionPlan(
            members=sub_plan_dict.get('members'),
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
        return sub_plans


sub_plan = CRUDSubscriptions()
