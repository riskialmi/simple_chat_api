import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base
from app.system.main import app
from app.db.database import get_db
from tests.api_objectivies import populate_data
from app.system.config import DATABASE_TEST_URL

PREFIX = '/api'

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_TEST_URL)
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
    room = populate_data.chat_room(sender_id=users[0], receiver_id=users[1], db=db)
    return {'sender_id': users[0], 'receiver_id': users[1], 'room': room}

@pytest.fixture
def conversation(db, initial_data):
    initial_data['messages'] = populate_data.messages(room=initial_data['room'],
                                                      sender_id=initial_data['sender_id'], db=db)
    return initial_data
