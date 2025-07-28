import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from app import models
from app.database import get_db, Base

from app.main import app

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

Base.metadata.create_all(bind=engine)
def get_override_db():

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_override_db

@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def clear_database_after_module():
    yield

    # Ensure tables exist before cleanup
    Base.metadata.create_all(bind=engine)

    db: Session = next(get_override_db())

    db.query(models.Sales).delete()
    db.query(models.Inventory).delete()
    db.query(models.Products).delete()
    db.query(models.Suppliers).delete()
    db.query(models.Categories).delete()
    db.query(models.Users).delete()

    try:
        db.execute(text("DELETE FROM sqlite_sequence;"))
    except Exception:
        pass

    db.commit()
    db.close()


