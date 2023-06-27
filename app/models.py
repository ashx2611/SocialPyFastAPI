from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__="Posts"
    id=Column(Integer,primary_key=True,nullable=False)
    Title=Column(String,nullable=False)
    Content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class User(Base):
    __tablename__= "Users"
    email=Column(String,nullable=False,unique=True) #prevents one email from registering twice
    password=Column(String,nullable=False)
    id=Column(Integer,primary_key=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



