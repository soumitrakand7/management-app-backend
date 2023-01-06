from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from datetime import datetime
from ..db.base_class import Base


class Users(Base):
    email = Column(String(32), unique=True, index=True,
                   primary_key=True, nullable=False)
    first_name = Column(String(32), index=True)
    last_name = Column(String(32))
    mobile_no = Column(String(10), index=True, nullable=False)
    address = Column(Text)
    hashed_password = Column(String(512))
    is_active = Column(Boolean(), default=False)
    profile_image_url = Column(Text)
    activation_code = Column(Float)
    registration_date = Column(DateTime, default=datetime.now())
    plan_id = Column(String(36), ForeignKey(
        "subscriptionplan.id", ondelete="CASCADE"))

    plan = relationship("SubscriptionPlan", back_populates="user")