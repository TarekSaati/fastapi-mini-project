from . import models
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# We want the client to adapt its posts to certain schemas depending on the HTTP request
class BasePost(BaseModel):
    title: str
    content: str

class CreatePost(BasePost):  
    published: bool = True
    rating: int
    
class UpdatePost(BasePost):
    published: bool

class BaseUser(BaseModel):
    email: EmailStr  


class UserOut(BaseUser):
    id: int
    email: EmailStr
    class Config():
        orm_mode = True

class ReturnedPost(BasePost):
    id: int
    published: bool
    created_at: datetime
    owner: UserOut
    
    class Config:
        orm_mode = True


class CreateUser(BaseUser):
    firstName: str
    lastName: str  
    password: str   


class UpdateUser(BaseUser):
    firstName: str
    lastName: str 
    password: str

class LoginCreds(BaseModel):
    email: EmailStr
    password: str

class OauthCreds(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    # constrained integer <= 1 e.i. {0, 1}
    dir: conint(le=1)

class VoteData(BaseModel):
    user_id: int
    post_id: int

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post: ReturnedPost
    votes: int

    class Config:
        orm_mode = True
