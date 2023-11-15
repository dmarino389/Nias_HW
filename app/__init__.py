from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure your database URI (e.g., SQLite, PostgreSQL, MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your database models using SQLAlchemy

if __name__ == '__main__':
    app.run()
