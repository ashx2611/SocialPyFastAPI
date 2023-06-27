from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models,oauth2
from ..database import get_db
from ..modelschema import PostCreate, PostResponse, PostUpdate

router=APIRouter(tags=['Posts'])                     
#order of the methods does matter as fast api shows the firsst 
#get decorator and matching url.
@router.get("/") #decorators used to convert the function into path operator.Sends a 'get;
#request to the api.
def root():
   return {"message":"Hello World,whats up?"}

@router.get("/posts",response_model=List[PostResponse])
def get_posts(db:Session=Depends(get_db)):
   #posts=cursor.execute('SELECT * FROM public."Posts"' )
   #cursor.fetchall()
   posts= db.query(models.Post).all()
   

   return posts

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def create_posts(post:PostCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
   # cursor.execute('INSERT INTO public."Posts"  ("Title","Content","Published")' 
   #  + 'values (%s,%s,%s)',(new_post.Title,new_post.Content,new_post.Published))
   # conn.commit()
   new_post=models.Post(**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   
   return new_post




   

@router.get("/posts/{id}",response_model=PostResponse)
def get_post(id:int,db:Session=Depends(get_db)):
   # print(type(id))
   # post=findpost(id)
   post=db.query(models.Post).filter(models.Post.id==id).first()

   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} not found.")
   
   return post

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
   # cursor.execute('Delete from public."Posts" where "ID"=%s returning *',(str(id),))

   # index=cursor.fetchone()
   # conn.commit()

   post=db.query(models.Post).filter(models.Post.id==id)
   if  post==None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {id} not found")

   post.delete(synchronize_session=False)
   db.commit()
  

@router.put("/posts/{id}",response_model=PostResponse)
def update_posts(id:int,post:PostUpdate,db:Session=Depends(get_db)):
   
      # cursor.execute('Update public."Posts" SET "Title"=%s, "Content"=%s,"Published"=%s where "ID"=%s',
      # post.Title,post.Content,post.Published,str(id))

      # post= cursor.fetchone()
      # conn.commit()
      post_query=db.query(models.Post).filter(models.Post.id==id)

      posts=post_query.first()

      if posts==None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} does not exist")
      post_query.update(post.dict(),synchronize_session=False)
      db.commit()

      return post_query.first()

