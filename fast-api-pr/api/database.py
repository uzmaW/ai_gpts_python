from typing import Generator
from sqlalchemy import text,Column, Integer, String

from sqlmodel import SQLModel, Field, Session, create_engine
from sqlalchemy.orm import sessionmaker, Session
from .settings import Settings as settings

from .data.models import User,Todo,JwtToken,Logger
from sqlalchemy import inspect
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import inspect
from sqlalchemy import event
from .security.crypto import pwd_context
import sqlalchemy

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
# Check if the database exists

#inspector = inspect(engine)
#database_exists = inspector.engine.dialect.has_database(engine, settings.SQLALCHEMY_DATABASE_URI)
# if not database_exists:
#     database_name = settings.SQLALCHEMY_DATABASE_URI.split("/")[-1]
#     engine.execute(f"CREATE DATABASE {database_name}")
#     print(f"Database {database_name} created successfully.")
class DatabaseNotFoundException(Exception):
    """Raised when the specified database does not exist."""
    pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}"
PS_USER = settings.PS_USER
PS_PASSWORD = settings.PS_PASSWORD
PS_SERVER = settings.PS_SERVER
PS_PORT = settings.PS_PORT

def seed_tables(target, connection, **kw):
    """if database is seeded then exit
    Args:
        target (_type_): _description_
        connection (_type_): _description_
    """
    if(connection.scalar(User.__table__.select().where(User.email == 'admin@example.com'))):
        return
    connection.execute(User.__table__.insert(), [
        {
            'email': 'admin@example.com',
            'hashed_password': pwd_context.hash('admin123'),
            'is_superuser': True
        }
    ])
    connection.execute(Todo.__table__.insert(), [
        {
            'title': 'Todo 1',
            'description': 'Description 1',
            'owner_id': 1
        },
        {
            'title': 'Todo 2',
            'description': 'Description 2',
            'owner_id': 1
        },
        {
            'title': 'Todo 3',
            'description': 'Description 3',
            'owner_id': 1
        }
    ])

event.listen(Todo.__table__, 'after_create', seed_tables)

    
def get_db()->Generator:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def create_tables(engine):
    SQLModel.metadata.create_all(bind=engine)

def drop_tables(engine):
    SQLModel.metadata.drop_all(bind=engine)

def setup_database():    
    try:   
        #print(" checking connection")
        """ create database if not exists then create tables """
    
        database_url = DATABASE_URL.format(
                            POSTGRES_USER=PS_USER,
                            POSTGRES_PASSWORD=PS_PASSWORD,
                            POSTGRES_SERVER=PS_SERVER,
                            POSTGRES_PORT=PS_PORT) 
  
        engine = create_engine(database_url)

        with engine.connect() as conn:
            conn.execute(text("COMMIT"))
            db_exists = conn.execute(text(f"select from pg_database where datname = '{settings.PS_DB}'"))
            
            if db_exists.fetchone() is None:
                print(f"Database {settings.PS_DB} does not exist. Creating...")
                conn.execute(text(f"CREATE DATABASE {settings.PS_DB}"))
            
            conn.execute(text("COMMIT"))
            conn.close()
            
            """ recreate engine with database """
            engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
            create_tables(engine)    
    except Exception as e:
        print(e)
    
     