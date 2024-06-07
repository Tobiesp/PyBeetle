from webapp import DB
from flask_login import UserMixin


class User(UserMixin, DB.Model):
    # TODO: Change primary key to GUID instead of integer
    id = DB.Column(DB.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = DB.Column(DB.String(100), unique=True)
    password = DB.Column(DB.String(100))
    name = DB.Column(DB.String(1000))