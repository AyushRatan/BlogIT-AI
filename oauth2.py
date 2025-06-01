import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime , timedelta, timezone
from schemas import TokenData
from fastapi import Depends,status,HTTPException
from database import get_db
from sqlalchemy.orm import Session
import models
from config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token:str,credential_exception):

    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        
        token_data = TokenData(id=id)
        
    except InvalidTokenError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token:str=Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access",headers={"WWW-Authenticate":"Bearer"})

    token_data =  verify_access_token(token,credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise credential_exception
    
    return user


   