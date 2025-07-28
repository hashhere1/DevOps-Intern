import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def get_engine():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hassaan:hassaan12@localhost:5432/inventory_system")

    if os.getenv("ENV") == "testing":
        DATABASE_URL = "sqlite:///:memory:"

    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    )

engine = get_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if os.getenv("ENV") != "testing":
    Base.metadata.create_all(bind=engine)
