from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_students_pagination():
    response = client.get("/students?page=1&limit=2")

    assert response.status_code == 200
    assert len(response.json()) <= 2


def test_get_student_by_id():
    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_student_not_found():
    response = client.get("/students/9999")

    assert response.status_code == 404


def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "email": "teststudent@gmail.com",
            "age": 20,
            "score": 8.5
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Student"


def test_create_duplicate_email():
    response = client.post(
        "/students",
        json={
            "name": "Student Test",
            "email": "a@gmail.com",
            "age": 20,
            "score": 8
        }
    )

    assert response.status_code == 400


def test_search_student():
    response = client.get(
        "/students/search?keyword=Nguyen"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_student():
    response = client.get(
        "/students/filter?min_score=7&max_score=9"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_student():
    response = client.put(
        "/students/1",
        json={
            "name": "Nguyen Van A Updated",
            "email": "a_updated@gmail.com",
            "age": 20,
            "score": 9
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Nguyen Van A Updated"


def test_update_student_not_found():
    response = client.put(
        "/students/9999",
        json={
            "name": "Test",
            "email": "test999@gmail.com",
            "age": 20,
            "score": 8
        }
    )

    assert response.status_code == 404


def test_delete_student_not_found():
    response = client.delete("/students/9999")

    assert response.status_code == 404


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
