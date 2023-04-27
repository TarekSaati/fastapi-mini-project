from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app import models, oauth2, utils

# 'postgresql://<username>:<password>@<host>/<DB name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/fastapi_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit = False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_users(session):
    users_data = [{
        'id': 1, 'email': 'tarek@gmail.com', 'firstName': 'tarek', 'lastName': 'saati', 'password': 'admin'
    },
    {
        'id': 2, 'email': 'sanjeev@gmail.com', 'firstName': 'san', 'lastName': 'jeev', 'password': 'tutor'
    }]
    
    def mapper(data):
        user = models.User(**data)
        user.password = utils.hash(data['password'])
        return user
    
    users = list(map(mapper, users_data))  
    session.add_all(users)
    session.commit()
    return users

@pytest.fixture
def token(test_users):
    return oauth2.create_access_token({'user_id': test_users[0].id})

@pytest.fixture
def authen_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_posts(session, test_users):
    posts_data = [{
        'id': 1, 'title': 'adfra', 'content': 'sdfaa', 'published': True, 'rating': 5
    },
    {
        'id': 2, 'title': '4564', 'content': 'sddffdfaa', 'published': False, 'rating': 4
    }]

    # mapping a post to each user
    def mapper(data, user):
        post = models.Post(**data)
        post.owner_id = user.id
        return post
    
    posts = list(map(mapper, posts_data, test_users))  
    session.add_all(posts)
    session.commit()
    return posts