import sys
import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}"
D2="/{POSTGRES_DB}?sslmode=disable"

def create_database(db_name=POSTGRES_DB):
    try:
        database_url = DATABASE_URL.format(
                            POSTGRES_USER=POSTGRES_USER,
                            POSTGRES_PASSWORD=POSTGRES_PASSWORD,
                            POSTGRES_SERVER=POSTGRES_SERVER,
                            POSTGRES_PORT=POSTGRES_PORT) #,                        POSTGRES_DB=db_name)

        engine = create_engine(database_url)
        metadata = MetaData()
        metadata.create_all(engine)
        conn = engine.connect()
        conn.execute(f"COMMIT")
        conn.execute(f"CREATE DATABASE {db_name}")
        conn.execute(f"COMMIT")
        conn.close()
        print(f"Database created: {db_name}")
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)    

def delete_database(database_url, db_name=POSTGRES_DB):
    try:
        database_url = DATABASE_URL.format(
                            POSTGRES_USER=POSTGRES_USER,
                            POSTGRES_PASSWORD=POSTGRES_PASSWORD,
                            POSTGRES_SERVER=POSTGRES_SERVER,
                            POSTGRES_PORT=POSTGRES_PORT,
                            POSTGRES_DB=db_name)

        # Create the engine
        engine = create_engine(database_url, echo=True)
        metadata = MetaData()
        metadata.reflect(engine)
        metadata.drop_all(engine)
        conn = engine.connect()
        conn.execute(f"COMMIT")
        conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
        conn.execute(f"COMMIT")
        conn.close()
        print(f"Database deleted: {db_name}")
    except Exception as e:
        print(f"Error deleting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ")
        print("----------------------------------------------------------------")
        print("       python cli.py <create/delete> <database_name>            ")
        print("----------------------------------------------------------------")
        print("")
        print("  if database name is empty it will create database from .env")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action not in ["--create", "--delete"]:
        print("Invalid action. Use 'create' or 'delete'.")
        sys.exit(1)
    if len(sys.argv) > 2:        
        database_name = sys.argv[2]
    else:
        database_name = POSTGRES_DB    

    if action == "--create":
        create_database(database_name)
    elif action == "--delete":
        delete_database(database_name)
    else:
        print("Invalid action. Use 'create' or 'delete'.")
        sys.exit(1)