import json
import pytest
import fastapi

from app.api import crud

def test_create_note(test_app, monkeypatch: pytest.MonkeyPatch):
    test_request_payload = {"title": "something", "description": "some description"}
    test_response_payload = {"id": 1, "title": "something", "description": "some description"}
    async def mock_post(payload):
        return 1
    
    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post('/notes/', data=json.dumps(test_request_payload))

    assert response.status_code == fastapi.status.HTTP_201_CREATED
    assert response.json() == test_response_payload

def test_create_note_invalid_json(test_app):
    # test missing description in body payload
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_app.post("/notes/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_note(test_app, monkeypatch: pytest.MonkeyPatch):
    test_data = {"id": 1, "title": "something", "description": "some description"}

    async def mock_get(id):
        return test_data
    
    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/notes/1')

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == test_data

def test_read_note_incorrect_id(test_app, monkeypatch: pytest.MonkeyPatch):
    async def mock_get(id):
        return None
    
    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/notes/999')
    assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"

    response  = test_app.get("/notes/0")
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY

def test_read_all_notes(test_app, monkeypatch: pytest.MonkeyPatch):
    mock_data = [
        {"id": 1, "title": "test title 1", "description": "test description 1"},
        {"id": 2, "title": "test title 2", "description": "test description 2"}
    ]
    async def mock_get_all():
        return mock_data

    monkeypatch.setattr(crud, 'get_all', mock_get_all)

    response = test_app.get('/notes/')

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == mock_data

def test_update_note(test_app, monkeypatch: pytest.MonkeyPatch):
    test_update_data = {"id": 1, "title": "something", "description": "some description"}

    async def mock_get(id):
        return True
    
    monkeypatch.setattr(crud, 'get', mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, 'put', mock_put)

    response = test_app.put('/notes/1/', data=json.dumps(test_update_data))

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == test_update_data

@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_delete_note(test_app, monkeypatch: pytest.MonkeyPatch):
    test_data = {"id": 1, "title": "something", "description": "some description"}

    async def mock_get(id):
        return test_data
    
    monkeypatch.setattr(crud, 'get', mock_get)

    async def mock_delete(id):
        return True

    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete('/notes/1/')

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == test_data


def test_delete_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999/")
    assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
