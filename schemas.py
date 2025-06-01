from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
from typing import Optional,Literal


class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content:Optional[str] = None
    published:Optional[bool] = None



class UserCreateResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class config:
        from_attributes=True



class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner:UserCreateResponse


    class config:
        from_attributes=True


class PostResponseWithVotes(BaseModel):
    post:PostResponse
    votes:int

    class config:
        from_attributes=True







class UserCreate(BaseModel):
    email:EmailStr
    password:str





class AuthLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int] = None



class VotePayload(BaseModel):
    post_id:int
    vote_dir:Literal[0,1]

