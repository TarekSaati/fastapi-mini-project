import pytest
from app import models, oauth2, schemas
from fastapi import HTTPException, status

def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'tarek@gmail.com', 'firstName': 'tarek', 'lastName': 'saati', 'password': 'admin'}
    )
    assert res.status_code == status.HTTP_201_CREATED
    out = schemas.UserOut(**res.json())
    assert out.email == 'tarek@gmail.com'

def test_login_user(client, test_users):
    res = client.post(
        '/login', data={'username': 'tarek@gmail.com', 'password': 'admin'}
    )
    assert res.status_code == status.HTTP_200_OK
    token = schemas.Token(**res.json())
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    tokenData = oauth2.verify_access_token(token.access_token, credentials_exception)
    data = schemas.TokenData(**tokenData.dict())
    assert data.id == test_users[0].id

@pytest.mark.parametrize('username, password, code', [
    ('false@gmail.com', 'admin', 404),
    ('tarek@gmail.com', 'fasle', 403),
    ('false@gmail.com', 'false', 404),
    ('eqwreeqw', 'asdasd', 422),
    ('asdasd', 'qweqwe', 422)
])
def test_incorrect_login_user(username, password, code, client, test_users):
    res = client.post(
        '/login', data={'username': username, 'password': password}
    )
    assert res.status_code == code
  
