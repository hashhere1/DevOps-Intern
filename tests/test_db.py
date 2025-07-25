from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

connection = engine.connect()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)

Base.metadata.create_all(bind=connection)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
