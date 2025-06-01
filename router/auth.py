from fastapi import APIRouter,status,Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AuthLogin, UserCreateResponse, Token
import models
import utils
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordBearer,OAuth2PasswordRequestForm



router = APIRouter(tags=["Auth"])

# According to Oauth2 the input should be in form data and should have fields (username,password)


@router.post("/login",status_code=status.HTTP_200_OK, response_model=Token)
async def login(loginform:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == loginform.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if utils.verify(loginform.password,user.password) == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    

    # generate token here
    token = oauth2.create_access_token(data={"user_id":user.id})


    return {"access_token":token,"token_type":"bearer"}
