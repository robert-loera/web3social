from fastapi.testclient import TestClient
import pytest
from app.database import SQLALCHEMY_DATABASE_URL
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base


# Make a test database so we dont have to use our main db

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:loera007@localhost:5432/web3social_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    # Dependency for sqlalchemy
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Create a fixture that will run before each testing functino by passing it
@pytest.fixture()
def client():
    # drop the tables
    Base.metadata.drop_all(bind=engine)
    # create all tables
    Base.metadata.create_all(bind=engine)
    # run code
    yield TestClient(app)
