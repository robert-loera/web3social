from .database import client
import pytest
from app import schemas
from jose import jwt
from app.config import settings
# fixture to create a user before we verify login


def test_create_user(client):
    res = client.post("/users/", json={"email": "example123@gmail.com",
                      "username": "example123", "password": "password"})
    print(res.json())
    assert res.json().get("username") == "example123"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    # validate the token (decode it)
    # verify the users token is correct by decoding token
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    # get field from auth.py we passed
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize('email, password, statuscode', [
    ('wrongemail@gmail.com', 'password', 403),
    ('robert@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password', 422),
    ('robert@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, statuscode):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == statuscode
    # assert res.json().get('detail') == 'Invalid Credentials'
