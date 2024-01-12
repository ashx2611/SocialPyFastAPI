
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
   email:EmailStr
   password:str

class UserOut(BaseModel):
   id:int
   email:EmailStr
   created_at:datetime

   class Config:
      orm_mode=True

      
class PostBase(BaseModel): 
   Title:str
   Content:str
   published:bool=True

class PostCreate(PostBase):
   pass

class PostUpdate(PostBase):
    Title:str
    Content:str
    published:bool
    owner_id:int

class PostResponse(PostBase):
   id:int
   Title:str
   published:bool
   created_at:datetime
   owner_id:int
   owner:UserOut

   class Config:
      orm_mode=True

class Vote(BaseModel):
   post_id:int
   dir:conint(le=1)
   
class PostOut(PostBase):
   Post :PostResponse
   votes:int

   class Config:
      orm_mode=True


def __init__():
   pass

class UserLogin(BaseModel):
   email: EmailStr
   password:str

class Token(BaseModel):
   access_token:str
   token_type:str

class TokenData(BaseModel):
   id:Optional[str]=None