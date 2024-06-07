import sys
from flask_sqlalchemy import SQLAlchemy

from webapp.settings import Settings

DB = SQLAlchemy()
SETTINGS: Settings = Settings()


def errPrint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)