import os


class Settings:
    SECRET_KEY = "qWMGso8lYDM5Hk2Dlmi-Kkth-clxTPZu_ctWjziiU4w"
    ACCESS_TOKEN_EXPIRE_MINUTES = int = 60 * 24 * 8
    SQL_USER = os.environ.get("SQL_USER", "root")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD", "abcd1234")
    SQL_HOST = os.environ.get(
        "SQL_HOST", "test-db.cnmbyuipzpkl.us-east-1.rds.amazonaws.com")
    SQL_DB = os.environ.get("SQL_DB", "db1")

    SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "soumitrakand3@gmail.com")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "ciekkwjqjmxuclcb")

    AWS_S3_ACCESS_KEY = os.environ.get(
        "AWS_S3_ACCESS_KEY", "AKIAXTI73LQPGCD3SDMZ")
    AWS_S3_SECRET_KEY = os.environ.get(
        "AWS_S3_SECRET_KEY", "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")


settings = Settings()
