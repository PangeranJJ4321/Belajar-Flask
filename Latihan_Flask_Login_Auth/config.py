# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flask_login_auth_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
