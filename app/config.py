import os
from typing import Type


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-12345")
    MYSQL_USER = os.environ.get("MYSQL_USER", "user")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "password")
    MYSQL_DB = os.environ.get("MYSQL_DB", "flask_db")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERS_PER_PAGE = 10


def get_config() -> Type[Config]:
    return Config
