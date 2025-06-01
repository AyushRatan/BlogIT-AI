from fastapi import APIRouter,HTTPException,status, Depends
from fastapi.responses import Response
from schemas import UserCreate,UserCreateResponse
from database import get_db
from sqlalchemy.orm import Session
import models
import utils 

router = APIRouter(prefix="/users",tags=["users"])




@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserCreateResponse)
async def create_user(user:UserCreate,db:Session=Depends(get_db)):

    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=UserCreateResponse)
async def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} not found")
    
    print(type(user))
    print(user.email)
    
    return user