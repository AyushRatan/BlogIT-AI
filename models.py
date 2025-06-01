from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer,String,Boolean,TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="true",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

    phone_number = Column(String,nullable=False)



class User(Base):

    __tablename__ = "users"
    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)


class Vote(Base):

    __tablename__ = "votes"

    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)