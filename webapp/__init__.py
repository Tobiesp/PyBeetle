import sys
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
SETTINGS = None


def errPrint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)