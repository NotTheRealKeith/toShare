# Lara's Code initializing the application

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Creating the database

db = SQLAlchemy()
DB_NAME = "database.db"


# Creating the app and using blue print to register our auth.py and views.py

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bornana'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Transaction

    create_database(app)

    # Using login manager to authorize users when logging into the app

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# Creating our database

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
