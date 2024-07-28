from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(20))
    role = db.Column(db.String(10), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(64))
    description = db.Column(db.String(256))
    date_posted = db.Column(db.Date)
    suggestion = db.Column(db.String(256))
    geolocation = db.Column(db.String(256))
    status = db.Column(db.String(20), default='Pending')
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'))
    rating = db.Column(db.Integer)
    suggestion = db.Column(db.String(256))
