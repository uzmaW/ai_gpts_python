import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.getenv('SECRET_KEY') or 'itsjust-another-app-$123456'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'localhost:5434'
    SQLALCHEMY_DATABASE_URI_DISABLE = os.getenv('DATABASE_URL_SSL_DISABLE') or 'localhost:5434'
    PS_DB = os.getenv('POSTGRES_DB') or 'postgres'
    PS_USER = os.getenv('POSTGRES_USER')
    PS_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    PS_SERVER = os.getenv('POSTGRES_SERVER')
    PS_PORT = os.getenv('POSTGRES_PORT')
    ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') or 30)
    ALGORITHM = os.getenv('ALGORITHM') or 'HS256'
    APP_NAME = os.getenv('APP_NAME') or ''
    APP_VERSION = os.getenv('APP_VERSION') or '1.0.0'
    APP_DESCRIPTION = os.getenv('APP_DESCRIPTION') or 'A simple application'
    DEBUG = os.getenv('DEBUG') or False
    #UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # simple mde  configurations
    #SIMPLEMDE_JS_IIFE = True
    #SIMPLEMDE_USE_CDN = True        

    