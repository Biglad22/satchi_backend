from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DB_Url = os.getenv("DATABASE_URL")
DB_engine = create_engine(DB_Url)
local_session =  sessionmaker(bind=DB_engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass


