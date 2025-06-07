from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import Optional
import models
from schemas import PostResponse, PostCreate, PostUpdate, PostResponseWithVotes
from typing import List
from database import get_db
from oauth2 import get_current_user



router = APIRouter(prefix="/posts",tags=["posts"])





@router.get("/",response_model=List[PostResponseWithVotes])
async def get_posts( db:Session = Depends(get_db),current_user:int = Depends(get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""select * from posts""")
    # data = cursor.fetchall()
    # all_posts = db.query(models.Post).filter(
    # func.to_tsvector('english', models.Post.title + ' ' + models.Post.content).op("@@")(func.websearch_to_tsquery("english",search))
    # )
    # all_posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
    all_posts = db.query(models.Post,func.count(models.Vote.post_id).label("vote_count")).join(models.Vote, models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()


    # print("*"*10)
    # print(all_posts)
    # print("*"*10)

    return [{"post":post,"votes":vote} for post,vote in all_posts]


@router.get("/{id}",response_model=PostResponse)
async def get_post_by_id(id:int,db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    # cursor.execute("""select * from posts where id=%s""",(id,))
    # data = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.post("/", response_model=PostResponse)
async def create_posts(post:PostCreate, db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    # cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning *""",(post.title,post.content,post.published))
    # inserted_data = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}",response_model=PostResponse)
async def update_post(id:int,update_post:PostUpdate,db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    # cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning * """,(post.title,post.content,post.published,str(id)))
    # updated_data = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Unable to update post, item with id={id} not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized")
    
    post_query.update(update_post.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(post)

    return post




@router.delete("/{id}",response_model=PostResponse)
async def delete_post(id:int, db:Session=Depends(get_db), current_user:models.User = Depends(get_current_user)):
    # cursor.execute("""delete from posts where id=%s returning * """,(id,))
    # deleted_item = cursor.fetchone()\

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized")
    
    post_query.delete()
    db.commit()
    

    # conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)