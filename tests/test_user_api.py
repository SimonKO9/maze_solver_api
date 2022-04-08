import json

from fastapi.testclient import TestClient

from app.main import app, get_user_service, get_persistence
from app.persistence.persistence import InMemoryPersistence
from app.user.user_service import UserService

client = TestClient(app)


def test_user_should_be_able_to_register():
    app.dependency_overrides[get_persistence] = lambda: InMemoryPersistence()

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert resp.json() == {
        'username': 'testuser'
    }


def test_return_400_if_user_already_exists():
    persistence = InMemoryPersistence()
    app.dependency_overrides[get_persistence] = lambda: persistence

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert resp.json() == {
        'username': 'testuser'
    }
    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 400
    assert resp.json() == {'message': 'User already exists.'}


def test_login_if_credentials_dont_match__should_return_403():
    app.dependency_overrides[get_persistence] = lambda: InMemoryPersistence()
    resp = client.post('/login', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 403
    assert resp.json() == {'message': 'Invalid credentials.'}


def test_login_if_credentials_dont_match__should_return_200_and_token():
    persistence = InMemoryPersistence()
    app.dependency_overrides[get_persistence] = lambda: persistence

    resp = client.post('/user', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200

    resp = client.post('/login', json.dumps({'username': 'testuser', 'password': 'passw0rd'}))
    assert resp.status_code == 200
    assert len(resp.json()['token']) > 0
