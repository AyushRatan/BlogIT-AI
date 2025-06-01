from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

connection_string = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.host}/{settings.database}"

engine = create_engine(connection_string,echo=True)
SessionLocal = sessionmaker(autoflush=False,bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:

#     try:

#         conn = psycopg2.connect(
#             host="localhost",
#             user="postgres",
#             password="postgres",
#             database="fastapi",
#             cursor_factory=RealDictCursor
#         )

#         cursor = conn.cursor()
#         logger.info("SUCCESSFULLY CONNECTED TO DATABASE")
#         break
#     except Exception as e:
#         logger.exception(e)