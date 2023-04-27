import pytest
from app import models, oauth2, schemas
from fastapi import HTTPException, status

def test_create_post(authen_client, test_users):
    res = authen_client.post(
        '/posts/', json={'title': 'adfra', 'content': 'sdfaa', 'published': True, 'rating': 5}
    )
    assert res.status_code == status.HTTP_201_CREATED
    out = schemas.ReturnedPost(**res.json())
    assert out.owner.id == test_users[0].id
    assert out.published == True
    assert out.content == 'sdfaa'

def test_update_post(authen_client, test_posts):
    res = authen_client.put(
        f'/posts/{test_posts[0].id}', json={'title': '13244', 'content': '8798', 'published': True}
    )
    assert res.status_code == status.HTTP_200_OK
    out = schemas.ReturnedPost(**res.json())
    assert out.owner.id == test_posts[0].owner_id

def test_delete_post(authen_client, test_posts):
    res = authen_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_vote(authen_client, session, token, test_posts, test_users):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    data = oauth2.verify_access_token(token,credentials_exception)
    user = session.query(models.User).filter(models.User.id == data.id).first()
    res = authen_client.post('/votes', json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 201
    vote = session.query(models.Vote).filter(models.Vote.post_id == 1).first()
    assert vote.user_id == user.id