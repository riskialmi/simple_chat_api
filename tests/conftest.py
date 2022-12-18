import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base
from app.system.main import app
from app.db.database import get_db
from tests.api_objectivies import populate_data

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
PREFIX = '/api'

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c

@pytest.fixture
def initial_data(db):
    users = populate_data.users(db)
    room = populate_data.room(sender=users[0], receiver=users[1], db=db)
    return {'sender': users[0], 'room': room}

@pytest.fixture
def conversation(db, initial_data):
    msg = populate_data.messages(room=initial_data['room'],  db=db)
    return {'sender': initial_data['sender'], 'room': initial_data['room']}
