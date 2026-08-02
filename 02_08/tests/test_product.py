from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_by_id():
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_product_not_found():
    response = client.get("/products/999")

    assert response.status_code == 404


def test_add_product():
    response = client.post(
        "/products",
        json={
            "name": "Macbook Air M4",
            "category": "Laptop",
            "price": 32000000,
            "quantity": 3
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Macbook Air M4"


def test_search_name():
    response = client.get(
        "/products/search/name?keyword=laptop"
    )

    assert response.status_code == 200


def test_search_category():
    response = client.get(
        "/products/search/category?category=Phone"
    )

    assert response.status_code == 200


def test_filter_price():
    response = client.get(
        "/products/filter?min_price=10000000&max_price=30000000"
    )

    assert response.status_code == 200
