from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all():
    response = client.get("/students")
    assert response.status_code == 200


def test_get_by_id():
    response = client.get("/students/1")
    assert response.status_code == 200


def test_get_not_found():
    response = client.get("/students/100")
    assert response.status_code == 404


def test_add_student():
    response = client.post(
        "/students",
        json={
            "name": "Le Van C",
            "age": 20,
            "email": "c@gmail.com"
        }
    )

    assert response.status_code == 201


def test_delete_not_found():
    response = client.delete("/students/999")
    assert response.status_code == 404
