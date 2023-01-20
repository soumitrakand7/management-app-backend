from sqlalchemy import Boolean, Column, DateTime, String, Text

from ..db.base_class import Base, default_pk


class SchedulerLog(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    job_name = Column(String(128), index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Boolean)
    log = Column(Text)
