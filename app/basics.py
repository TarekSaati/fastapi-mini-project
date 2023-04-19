# FastApi_tutorial
from random import randrange
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None

posts = [{'title': 'post1 title', 'context' : 'post1 context', 'id':1}, \
         {'title': 'post2 title', 'context' : 'post2 context', 'id':2}]

@app.get('/')
async def root():
    return 'Hello World'

@app.get('/posts/')
def get_posts():
    return posts

'''
@app.post('/createposts')
def create_posts(args: dict = Body(...)):
    print(args)
    return f"title: {args['message']}"
'''
# we must set status to 201
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    posts.append(post_dict)
    return post_dict

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int):
    for i in range(len(posts)):
        post = posts[i]
        if post['id'] == id:
            posts.pop(i)

@app.get('/posts/{id}')
# an integer is required as ID with error log returned to client when not 
# Be ware of mis-matching with other get\post routs (e.g. get('/posts/latest')) 
def get_posts(id: int):
    # FastApi will serialize (dump) posts to JSON format
    for pst in posts:   
        if pst['id'] == id:
            return (pst)
    # if post id not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='404 - not found')

