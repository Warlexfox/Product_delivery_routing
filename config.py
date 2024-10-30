import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a3f1c8e8d1b2f4c5d6e7f8a9b0c1d2e3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
