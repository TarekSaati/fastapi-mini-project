# Postgres_tutorial
from typing import List
from fastapi import HTTPException, status, Depends, APIRouter
import psycopg2 as pg
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db

# models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/users', tags=["Users"])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    # refresh to get back the nesw_post variable after the ADD method
    db.refresh(new_user)
    return (new_user)

@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, upd_user: schemas.UpdateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
    upd_user.password = utils.hash(upd_user.password)
    user.update(upd_user.dict())
    db.commit()
    return user.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
    user.delete(synchronize_session=False)
    db.commit()
    return f'Succesfully deleted user {id}'