from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2
from ..database import get_db
from ..modelschema import PostCreate, PostOut, PostResponse, PostUpdate

router=APIRouter(tags=['Posts'])                     
#order of the methods does matter as fast api shows the firsst 
#get decorator and matching url.
#decorators used to convert the function into path operator.Sends a 'get;
#request to the api.


@router.get("/posts",response_model=List[PostOut])
def get_posts(db:Session=Depends(get_db),search:Optional[str]="", skip:int =0, limit:int =10,current_user:int =Depends(oauth2.get_current_user)):


   posts= db.query(models.Post).limit(limit).all()
   
   posts=db.query(models.Post).filter(models.Post.Title.contains(search).limit(limit).offset(skip).all())

   posts=db.query(models.Post,func.count(models.Votes.posts_id).label("votes")).join(models.Votes,models.Votes.posts_id==models.Post.id , isouter=True)
   
   
   if posts.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action.")
   return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def create_posts(post:PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):

   
   new_post=models.Post(owner_id=user_id.id,**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   
   return new_post




   

@router.get("/posts/{id}",response_model=PostOut)
def get_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
   
   post=db.query(models.Post).filter(models.Post.id==id).first()

   post=db.query(models.Post,func.count(models.Votes.posts_id).label("votes")).join(models.Votes,models.Votes.posts_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first() 

   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} not found.")
   
   

   return post



@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
   

   post_query=db.query(models.Post).filter(models.Post.id==id)
   
   post=post_query.first()
   
   if  post==None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {id} not found")
   
   if post.owner_id != user_id.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action.")
   post_query.delete(synchronize_session=False)
   db.commit()
  

@router.put("/posts/{id}",response_model=PostResponse)
def update_posts(id:int,post:PostUpdate,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
   
      
      post_query=db.query(models.Post).filter(models.Post.id==id)

      posts=post_query.first()

      if posts==None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} does not exist")
      if post.owner_id !=current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action.")  
         
      post_query.update(post.dict(),synchronize_session=False)
      db.commit()

      return post_query.first()

