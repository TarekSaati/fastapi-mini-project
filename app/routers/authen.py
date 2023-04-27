from fastapi import HTTPException, status, Depends, APIRouter
from .. import utils, database, models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/login', tags=['Authentication'])

@router.post('/', response_model=schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        schemas.OauthCreds(**creds.__dict__)
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Wrong Entries')
    user = db.query(models.User).filter(creds.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication error')
    elif not utils.verify(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Authentication error')
    
    access_token = oauth2.create_access_token({'user_id': user.id})
    return {'access_token': access_token, 'token_type': "bearer" }

