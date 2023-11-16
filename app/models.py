# models.py (Defining SQLAlchemy models)
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    medical_records = db.Column(db.Text)

    def __repr__(self):
        return f'<FamilyMember {self.name}>'