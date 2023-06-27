import time

import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import auth, post, users

models.Base.metadata.create_all(bind=engine)
app= FastAPI()
#keep connecting until connection is established
while True:
   try:
      conn=psycopg2.connect(host='localhost',database='fastapidb',user='postgres',password='timber'
      ,cursor_factory=RealDictCursor)
      cursor=conn.cursor()
      print("Connected to database")
      break
   except Exception as error:
      print("Connecting to database failed")
      print("Error was ",error)
      time.sleep(2)

app.include_router(post.router)
app.include_router(auth.router)
app.include_router(users.router)





   
