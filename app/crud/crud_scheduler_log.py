from typing import Any

from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import SchedulerLog


class CRUDSchedulerLog(CRUDBase):
    def create(self, db: Session, *, job_name: str, start_time: Any, end_time: Any, status: Any, log: str):
        scheduler_log_obj = SchedulerLog(
            job_name=job_name,
            start_time=start_time,
            end_time=end_time,
            status=status,
            log=log
        )
        db.add(scheduler_log_obj)
        db.commit()
        db.refresh(scheduler_log_obj)
        return scheduler_log_obj


scheduler_log = CRUDSchedulerLog()
