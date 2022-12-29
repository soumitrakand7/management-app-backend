from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

sql_user = settings.SQL_USER
sql_password = settings.SQL_PASSWORD
sql_host = settings.SQL_HOST
sql_db = settings.SQL_DB

sql_connection_str = "sqlite:///./sql_app.db"


# sql_connection_str = "postgresql+psycopg2://{sql_user}:{sql_password}@{sql_host}/{sql_db}".format(
#     sql_user=sql_user,
#     sql_password=sql_password,
#     sql_host=sql_host,
#     sql_db=sql_db
# )

engine = create_engine(
    sql_connection_str, pool_pre_ping=True, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
