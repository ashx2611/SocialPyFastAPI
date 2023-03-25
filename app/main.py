from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response,status,HTTPException
app= FastAPI()


class Post(BaseModel): 
   title:str
   content:str
   published:bool=True
   rating:Optional[int]=None

my_posts=[{"title":"This is example post 1","content":"this is sample post","id":1}
,{"title":"This is example post 2","content":"this is sample post 2","id":2},{"title":"This is example post 3","content":"this is sample post 3","id":3}]

#order of the methods does matter as fast api shows the firsst 
#get decorator and matching url.
@app.get("/") #decorators used to convert the function into path operator.Sends a 'get;
#request to the api.
def root():
   return {"message":"Hello WOrld,whats up heeeeee?"}

@app.get("/posts")
def get_posts():

   return{"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
#title:str, content:str,category:str, Ispublished:bool
def create_posts(new_post:Post):
   post_dict=new_post.dict()
   post_dict['id']=randrange(0,1000000)
   my_posts.append(post_dict)
   return {"data":post_dict}

def findpost(id:int):
   for p in my_posts:
      if p['id'] ==id:
         return p
def find_index_post(id:int):
   for i,p in enumerate(my_posts):
      if p['id']==id:
         return i

   

@app.get("/posts/{id}")
def get_post(id:int):
   print(type(id))
   post=findpost(id)
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} not found.")
   
   return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
   index=find_index_post(id)
   if  index==None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {id} not found")

   my_posts.pop(index)
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
   index=find_index_post(id)
   if  index==None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {id} not found")
   post_dict= post.dict()
   post_dict['id']=id
   my_posts[index]=post_dict

   
   return {"data":post_dict}


   
   




