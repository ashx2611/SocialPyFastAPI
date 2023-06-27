from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, utils
from ..database import get_db
from ..modelschema import UserCreate, UserOut

router=APIRouter(prefix="/users",tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
   try:
      user.password=utils.gethash(user.password)
      new_user=models.User(**user.dict())
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
   except:
      return new_user

   return new_user



@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_user(id:int,db:Session=Depends(get_db)):
   user=db.query(models.User).filter(models.User.id==id).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id: {id} not found")

   return {user}