from fastapi import FastAPI, Response,status, Depends
import logging
from sqlalchemy.orm import Session
from database import engine,get_db
from router import posts,users,auth,votes
import models
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(levelname)s in %(name)s: %(message)s')


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/sqlalchemy")
async def check_connection(db:Session = Depends(get_db)):
    return {"msg":"connected to server"}


@app.get("/ping")
async def server_check():
    return Response(status_code=status.HTTP_200_OK,content="Pong!")

