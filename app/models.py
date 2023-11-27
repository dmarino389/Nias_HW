# models.py (Defining SQLAlchemy models)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)




class FamilyMember(db.Model):
    # Existing columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    birthdate = db.Column(db.Text(100), nullable = False)
    medical_records = db.Column(db.Text)
    notes = db.Column(db.Text(600))

    def __repr__(self):
        return f'<FamilyMember {self.name}>'
