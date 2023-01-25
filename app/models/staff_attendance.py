from sqlalchemy import Boolean, Column, String, Text, DateTime, Float, ForeignKey, Time, Date
from sqlalchemy.orm import relationship
from ..db.base_class import default_pk

from ..db.base_class import Base


class StaffAttendance(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    staff_id = Column(String(36), ForeignKey("staffmember.id"))
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    date = Column(Date)
    status = Column(String(32))

    staff_member = relationship("StaffMember", foreign_keys=[staff_id])
