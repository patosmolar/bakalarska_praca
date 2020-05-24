"""This is the models module.

Provides User class for database.
"""
from datetime import datetime
from bakalarka import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """Query to ged user by ID"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model.

    Attributes:
        id (int): PK in database.
        username (str): Username of user.
        email (str): Email of user.
        password (str): Password of user, crypted by Bcrypt.
        calendarID (str): ID of Google Calendar to work with scheduler. 
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True, default="-1")
    calendarID = db.Column(db.String(60))
    

    def __repr__(self):
        """Function to print info about User"""
        return f"User('{self.username}', '{self.email}')"

