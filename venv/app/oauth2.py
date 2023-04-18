from urllib.parse import scheme_chars
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import utils, database, models, schemas
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_sceme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    cdata = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    cdata.update({'exp': expire})
    encoded_jwt = jwt.encode(cdata, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get('user_id')
    if not id:
        raise credentials_exception
    return schemas.TokenData(id=id)

def get_current_user(token: str = Depends(oauth2_sceme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    data = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == data.id).first()

    return user


