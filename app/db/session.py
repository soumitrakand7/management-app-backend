from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from app.crud import scheduler_log

import traceback
from datetime import datetime

sql_user = settings.SQL_USER
sql_password = settings.SQL_PASSWORD
sql_host = settings.SQL_HOST
sql_db = settings.SQL_DB

sql_connection_str = "sqlite:///./sql_app.db"


sql_connection_str = "postgresql+psycopg2://{sql_user}:{sql_password}@{sql_host}/{sql_db}".format(
    sql_user=sql_user,
    sql_password=sql_password,
    sql_host=sql_host,
    sql_db=sql_db
)

engine = create_engine(
    sql_connection_str, pool_pre_ping=True, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

db = SessionLocal()


def create_scheduler_log(job_name):
    def inner(func):
        def wrap(*args, **kwargs):
            start_time = datetime.str(
                datetime.now(tz=ZoneInfo('Asia/Kolkata')))
            try:
                response = func(*args, **kwargs)
                status = 1
                log = None
            except Exception as e:
                response = None
                status = 0
                log = traceback.format_exc()
            end_time = datetime.str(datetime.now(tz=ZoneInfo('Asia/Kolkata')))
            scheduler_log.create(db=db, job_name=job_name, start_time=start_time,
                                 end_time=end_time, status=status, log=log)
            return response
        return wrap
    return inner
