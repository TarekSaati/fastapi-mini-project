from app.calcs import scale, Post
import pytest

@pytest.fixture()
def post():
    return Post()


@pytest.mark.parametrize('num, expected', [
    (5, 6),
    (3.33, 1.2*3.33),
    (4/3, 1.6)
])
def test_scale(num, expected):
    assert round(scale(num), 5) == expected

def test_add_content_post(post):
    post.add_content("text")
    assert post.content == "text"

def test_like_post(post):
    post.change_status(1)
    post.change_status(-1)
    assert post.status == 0