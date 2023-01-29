from sqlalchemy import Boolean, Column, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base_class import Base, default_pk


class StaffLeave(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    staff_id = Column(String(36), ForeignKey("staffmember.id"))
    leave_subject = Column(String(36), nullable=False, index=True)
    reason = Column(Text)
    starting_date = Column(DateTime)
    ending_date = Column(DateTime)
    status = Column(String(32), nullable=False)
    staff_member = relationship("StaffMember", foreign_keys=[staff_id])
