from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from datetime import datetime
from ..db.base_class import Base


class SubscriberGroup(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    admin_email = Column(String(36), ForeignKey("users.email"))
    plan_id = Column(String(36), ForeignKey("subscriptionplan.id"))
    created_at = Column(DateTime, default=datetime.now())
    valid_until = Column(DateTime, nullable=False)
    member_count = Column(Float, nullable=False, index=True)

    admin = relationship("Users", foreign_keys=[admin_email])
    subscription_plan = relationship(
        "SubscriptionPlan", foreign_keys=[plan_id])
