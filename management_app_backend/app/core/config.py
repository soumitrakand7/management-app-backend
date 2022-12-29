import os


class Settings:
    SECRET_KEY = "qWMGso8lYDM5Hk2Dlmi-Kkth-clxTPZu_ctWjziiU4w"
    ACCESS_TOKEN_EXPIRE_MINUTES = int = 60 * 24 * 8
    SQL_USER = os.environ.get("SQL_USER", "user3")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD", "soumitra3520")
    SQL_HOST = os.environ.get(
        "SQL_HOST", "localhost")
    SQL_DB = os.environ.get("SQL_DB", "management_db")


settings = Settings()
