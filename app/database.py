import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal =sessionmaker(autocommit=False,bind=engine,autoflush=False)

Base=declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#    try:
#       conn=psycopg2.connect(host='localhost',database='fastapidb',user='postgres',password='timber'
#       ,cursor_factory=RealDictCursor)
#       cursor=conn.cursor()
#       print("Connected to database")
#       break
#    except Exception as error:
#       print("Connecting to database failed")
#       print("Error was ",error)
#       time.sleep(2)
