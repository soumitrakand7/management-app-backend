from sqlalchemy import Boolean, Column, String, Text, Float
from ..db.base_class import default_pk
from sqlalchemy.orm import relationship, backref

from ..db.base_class import Base


class SubscriptionPlan(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    plan_name = Column(String(36), nullable=False)
    min_members = Column(Float)
    max_members = Column(Float)
    price = Column(Float)
