from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# In-memory database (shared)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ✅ Shared connection
connection = engine.connect()

# ✅ Bind session to this connection
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)

# ✅ Create all tables once on shared connection
Base.metadata.create_all(bind=connection)

# ✅ Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
