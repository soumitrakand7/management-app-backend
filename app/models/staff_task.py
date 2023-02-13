from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class StaffTask(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    task_title = Column(String(36), nullable=False, index=True)
    description = Column(Text)
    assigned_at = Column(DateTime)
    valid_for = Column(Float)
    valid_from = Column(DateTime)
    priority = Column(String(24), nullable=False)
    status = Column(String(36))  # Active / Cancelled / Completed / Expired

    subscriber_group_id = Column(String(36), ForeignKey(
        "subscribergroup.id"))

    subscriber_group = relationship(
        "SubscriberGroup", foreign_keys=[subscriber_group_id])
