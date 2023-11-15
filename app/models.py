# models.py (Defining SQLAlchemy models)
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class FamilyHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    # Define other fields for your FamilyHistory model

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        # Initialize other fields as needed


# models.py
class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    medical_records = db.Column(db.Text)
    birthdate = db.Column()

    def __repr__(self):
        return f'<FamilyMember {self.name}, {self.relationship}>'
