# config.py

import os

class Config:
    SECRET_KEY = 'letsworldtheworld'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
