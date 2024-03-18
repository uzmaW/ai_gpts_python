from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from settings import Settings as settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables(engine):
    Base.metadata.create_all(bind=engine)

def drop_tables(engine):
    Base.metadata.drop_all(bind=engine)

def setup_database(db:Session):
    try:        
        create_tables(engine)
        # add default user
     
    except Exception as e:
        print(e)            