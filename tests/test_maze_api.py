from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
import json
from app.main import app, get_user_service, get_user
from app.user.user_service import UserService

client = TestClient(app)

app.dependency_overrides[get_user] = lambda: 'test1'


def test_create_maze_should_succeed_for_valid_maze():
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4",
                  "B5", "E5", "B6", "D6",
                  "E6", "G6", "H6", "B7", "D7", "G7", "B8"],
    }
    resp = client.post('/maze', json=payload)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json['entrance'] == payload['entrance']
    assert resp_json['gridSize'] == payload['gridSize']
    assert resp_json['walls'] == payload['walls']
    assert resp_json['id'] is not None


def test_create_maze_should_fail_for_entrance_out_of_bounds():
    payload = {
        "entrance": "D1",
        "gridSize": "3x3",
        "walls": ["B1", "B2", "B3"],
    }
    resp = client.post('/maze', json=payload)
    assert resp.status_code == 422
    assert resp.json()['detail'][0]['msg'] == 'Entrance is not within bounds.'


def test_create_maze_should_fail_for_wall_out_of_bounds():
    payload = {
        "entrance": "A1",
        "gridSize": "3x3",
        "walls": ["B1", "B2", "B4"],
    }
    resp = client.post('/maze', json=payload)
    assert resp.status_code == 422
    assert resp.json()['detail'][0]['msg'] == 'Wall B4 is not within bounds.'


def test_create_maze_should_fail_for_invalid_grid_size():
    payload = {
        "entrance": "A1",
        "gridSize": "123",
        "walls": ["B1", "B2", "B4"],
    }
    resp = client.post('/maze', json=payload)
    assert resp.status_code == 422
    assert resp.json()['detail'][0]['msg'] == 'string does not match regex "[1-9][0-9]*x[1-9][0-9]*"'


def test_get_solution_with_invalid_steps_returns_400():
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4",
                  "B5", "E5", "B6", "D6",
                  "E6", "G6", "H6", "B7", "D7", "G7", "B8"],
    }
    resp = client.post('/maze', json=payload)
    id = resp.json()['id']

    resp = client.get(f'/maze/{id}/solution?steps=whatever')
    assert resp.status_code == 422


def test_get_min_solution_should_return_path():
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4",
                  "B5", "E5", "B6", "D6",
                  "E6", "G6", "H6", "B7", "D7", "G7", "B8"],
    }
    resp = client.post('/maze', json=payload)
    id = resp.json()['id']

    resp = client.get(f'/maze/{id}/solution?steps=min')
    assert resp.status_code == 200
    assert resp.json() == ['A1', 'B1', 'B2', 'B3', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']


def test_get_max_solution_should_return_path():
    payload = {
        "entrance": "A1",
        "gridSize": "8x8",
        "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4",
                  "B5", "E5", "B6", "D6",
                  "E6", "G6", "H6", "B7", "D7", "G7", "B8"],
    }
    resp = client.post('/maze', json=payload)
    id = resp.json()['id']

    resp = client.get(f'/maze/{id}/solution?steps=max')
    assert resp.status_code == 200
    assert resp.json() == ['A1', 'B1', 'B2', 'B3', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']


def test_get_solution_for_maze_without_one_should_return_500():
    payload = {
        "entrance": "A1",
        "gridSize": "4x4",
        "walls": ["A2", "B2", "C2", "D2"],
    }
    resp = client.post('/maze', json=payload)
    id = resp.json()['id']

    resp = client.get(f'/maze/{id}/solution?steps=min')
    assert resp.status_code == 500
    assert resp.json() == {'detail': 'No exit found.'}


def test_get_solution_for_maze_with_multiple_exits_should_return_500():
    payload = {
        "entrance": "A1",
        "gridSize": "4x4",
        "walls": [],
    }
    resp = client.post('/maze', json=payload)
    id = resp.json()['id']

    resp = client.get(f'/maze/{id}/solution?steps=min')
    assert resp.status_code == 500
    assert resp.json() == {'detail': 'Multiple exits detected: A4, B4, C4, D4.'}