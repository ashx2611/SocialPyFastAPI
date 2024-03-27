
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models

from .config import Settings
from .database import engine
from .routers import auth, post, users, vote

#models.Base.metadata.create_all(bind=engine)
app= FastAPI()
origins=["*"]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
#keep connecting until connection is established


@app.get("/")
def root():
   return{"message":"Hello! Welcome to the website!!"}
app.include_router(post.router)

app.include_router(auth.router)

app.include_router(users.router)

app.include_router(vote.router)


   
