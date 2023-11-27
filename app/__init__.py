from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from .models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app) 
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import User here to avoid circular import
    return User.query.get(int(user_id))

# Import routes and models after creating db
from app import routes, models
