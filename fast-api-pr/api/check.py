from fastapi import FastAPI
import uvicorn
from settings import Settings as settings
import logging
from controllers.User import router as user_router
from controllers.Todos import router as todos_router
from controllers.TokenManager import router as token_manager_router
from database import setup_database,get_db
#from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine,inspect
import sqlalchemy


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
app: FastAPI = FastAPI()

app.title = settings.APP_NAME
app.description = settings.APP_DESCRIPTION
app.version = settings.APP_VERSION
app.debug = bool(settings.DEBUG)
#app.docs_url = settings.DOCS_URL

# prepare database
print("check")
try:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    # Check if the database exists
    inspector = inspect(engine)
    database_exists = inspector.has_schema(settings.PS_DB)
    #dialect.has_schema(engine, settings.SQLALCHEMY_DATABASE_URI)
    print(database_exists)
    print(sqlalchemy.database_exists(engine.url))
    print(engine.url)
except Exception as e:
   print(e.args)
exit()
if not sqlalchemy.database_exists(engine.url):

    with engine.connect() as conn:
        conn.execute("commit")
        conn.execute("create database test")
exit


exit()

print("end")

@app.get("/")
def index():
    return {"message": "FastAPI : Todo App"}

"""_auto run server from code_"""
#if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)