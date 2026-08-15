import pytest

from app import app
from inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Inventory Management API is running!"


def test_get_items(client):
    response = client.get("/items")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)


def test_get_single_item(client):
    response = client.get("/items/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1


def test_create_item(client):
    new_item = {
        "name": "Test Product",
        "category": "Testing",
        "price": 100,
        "quantity": 10,
        "barcode": "999888777"
    }

    response = client.post(
        "/items",
        json=new_item
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Test Product"
    assert data["category"] == "Testing"
    assert data["price"] == 100
    assert data["quantity"] == 10
    assert data["barcode"] == "999888777"


def test_update_item(client):
    response = client.patch(
        "/items/1",
        json={
            "price": 500,
            "quantity": 20
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 500
    assert data["quantity"] == 20


def test_delete_item(client):
    response = client.delete("/items/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item deleted successfully"


def test_get_nonexistent_item(client):
    response = client.get("/items/99999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"


def test_create_item_missing_field(client):
    incomplete_item = {
        "name": "Incomplete Product",
        "price": 100
    }

    response = client.post(
        "/items",
        json=incomplete_item
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_item_count(client):
    response = client.get("/items/count")

    assert response.status_code == 200

    data = response.get_json()

    assert "count" in data
    assert isinstance(data["count"], int)


def test_search_product(client, monkeypatch):
    fake_product = {
        "product_name": "Test Nutella",
        "brands": "Ferrero",
        "categories": "Spreads",
        "quantity": "350g",
        "image_url": "https://example.com/image.jpg"
    }

    def mock_get_product(barcode):
        return fake_product

    monkeypatch.setattr(
        "app.get_product_by_barcode",
        mock_get_product
    )

    response = client.get(
        "/search?barcode=3017620422003"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["product_name"] == "Test Nutella"
    assert data["brands"] == "Ferrero"
    assert data["barcode"] == "3017620422003"


def test_search_product_without_barcode(client):
    response = client.get("/search")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Barcode is required"


def test_import_product(client, monkeypatch):
    fake_product = {
        "product_name": "Imported Test Product",
        "categories": "Test Category"
    }

    def mock_get_product(barcode):
        return fake_product

    monkeypatch.setattr(
        "app.get_product_by_barcode",
        mock_get_product
    )

    response = client.post(
        "/import/123456789"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Product imported successfully"

    item = data["item"]

    assert item["name"] == "Imported Test Product"
    assert item["category"] == "Test Category"
    assert item["barcode"] == "123456789"


def test_import_product_not_found(client, monkeypatch):

    def mock_get_product(barcode):
        return None

    monkeypatch.setattr(
        "app.get_product_by_barcode",
        mock_get_product
    )

    response = client.post(
        "/import/000000000"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Product not found"