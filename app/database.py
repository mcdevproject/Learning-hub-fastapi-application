# Using SQLAlchemy ORM for query
# Python code <--Python--> ORM (SQLAlchemy) <--SQL--> PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Using SQLALCHEMY:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
# DB conncetion module: with SQL
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:  # DB Connection Try-Except
    try:
        db_connection = psycopg2.connect(host='localhost', database='fastapi',
                                         user='postgres', password='8888', cursor_factory=RealDictCursor)
        cursor = db_connection.cursor()
        print("DB: Connection Sucessful.")
        break
    except Exception as error:
        print(f"DB: Connection Fail. Error: {error}")
        time.sleep(2)"""
