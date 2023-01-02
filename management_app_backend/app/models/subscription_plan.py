from sqlalchemy import Boolean, Column, String, Text, Float
from ..db.base_class import default_pk

from ..db.base_class import Base


class SubscriptionPlan(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    plan_name = Column(String(36), nullable=False)
    members = Column(Float)
    price = Column(Float)
