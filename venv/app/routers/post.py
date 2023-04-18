# Postgres_tutorial
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import psycopg2 as pg
from sqlalchemy import func
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

# no need with alembic!
# models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/posts', tags=["Posts"])

# try: 
#     conn = pg.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
# except Exception as e:
#     print(e)   

## When returning a LIST of classes we can use typing.List variable 
@router.get('/', response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts;''')
    # posts = cursor.fetchall()
    # return posts
    # db.query(models) returns the SQL code behind!
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    
    results = list ( map (lambda x : x._mapping, results) )
    return results


# we must set status to 201
## client-data schema is fed into the function, while api-data schema is fed into the decorator  
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnedPost)
def create_posts(post: schemas.CreatePost, 
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # for securety reasons post info must be passed with placeholders (%s)
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *;""", (post.title, post.content))
    # conn.commit()
    # return cursor.fetchone()
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    # refresh to get back the new_post variable after the ADD method
    db.refresh(new_post)
    return (new_post)

@router.put('/{id}', response_model=schemas.ReturnedPost)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='prohibited access')
    post.update(updated_post.dict())
    db.commit()
    return post.first()


@router.get('/{id}', response_model=schemas.PostVote)
# an integer is required as ID with error log returned to client when not 
# Be ware of mis-matching with other get\post routs (e.g. get('/posts/latest')) 
def get_posts(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s RETURNING *;""", (str(id)))
    # return cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='prohibited access')
    post.delete(synchronize_session=False)
    db.commit()