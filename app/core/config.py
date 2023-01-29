import os


class Settings:
    SECRET_KEY = "qWMGso8lYDM5Hk2Dlmi-Kkth-clxTPZu_ctWjziiU4w"
    ACCESS_TOKEN_EXPIRE_MINUTES = int = 60 * 24 * 8
    SQL_USER = os.environ.get("SQL_USER", "root")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD", "abcd1234")
    SQL_HOST = os.environ.get(
        "SQL_HOST", "test-db.cnmbyuipzpkl.us-east-1.rds.amazonaws.com")
    SQL_DB = os.environ.get("SQL_DB", "db1")

    ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID", "AKIAXTI73LQPGCD3SDMZ")
    SECRET_ACCESS_KEY = os.environ.get(
        "SECRET_ACCESS_KEY", "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")
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "soumitrakand3@gmail.com")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "ciekkwjqjmxuclcb")


settings = Settings()
