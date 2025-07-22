from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATA_BASE_URL =os.getenv("postgresql://hassaan:hassaan12@localhost:5432/inventory_system")

engine = create_engine(DATA_BASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit= False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()