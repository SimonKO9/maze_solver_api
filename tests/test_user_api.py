from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
import json
from app.main import app, get_user_service
from app.user.user_service import UserService

client = TestClient(app)


def test_user_should_be_able_to_register():
    app.dependency_overrides[get_user_service] = lambda: UserService()

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert resp.json() == {
        'username': 'testuser'
    }


def test_return_400_if_user_already_exists():
    service = UserService()
    app.dependency_overrides[get_user_service] = lambda: service

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert resp.json() == {
        'username': 'testuser'
    }
    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'User already exists.'}


def test_login_if_credentials_dont_match__should_return_401():
    app.dependency_overrides[get_user_service] = lambda: UserService()
    resp = client.post('/login', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 401
    assert resp.json() == {'detail': 'Invalid credentials.'}


def test_login_if_credentials_dont_match__should_return_200_and_token():
    service = UserService()
    app.dependency_overrides[get_user_service] = lambda: service

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200

    resp = client.post('/login', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert len(resp.json()['token']) > 0
