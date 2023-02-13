from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
from ..db.base_class import Base
from backports.zoneinfo import ZoneInfo


class Users(Base):
    email = Column(String(32), unique=True, index=True,
                   primary_key=True, nullable=False)
    full_name = Column(String(64), nullable=False, index=True)
    mobile_no = Column(String(10), index=True, nullable=True)
    address = Column(Text)
    hashed_password = Column(String(512))
    is_active = Column(Boolean(), default=False)
    profile_image_url = Column(Text, nullable=True)
    activation_code = Column(Float)
    registration_date = Column(DateTime, default=str(
        datetime.now(tz=ZoneInfo('Asia/Kolkata'))))
    profile = Column(String(36), index=True)  # admin / staff / guest / family
    bank_ifsc = Column(Text)
    bank_account_no = Column(Text)

    subscriber_group_id = Column(String(36), ForeignKey(
        "subscribergroup.id"), nullable=True)

    subscriber_group = relationship(
        "SubscriberGroup", foreign_keys=[subscriber_group_id])
