# test_inventory_api.py
import os
os.environ["INVENTORY_DB"] = "test_inventory.db"   # before importing the app
import pytest
from inventory_api import app

KEY = {"X-API-Key": "dev-key-change-me"}

@pytest.fixture
def client():
    return app.test_client()

def test_create_and_get(client):
    r = client.post("/api/assets", json={"tag": "T-1", "name": "Test", "category": "laptop"}, headers=KEY)
    assert r.status_code == 201
    assert client.get("/api/assets/T-1").get_json()["name"] == "Test"

def test_needs_key(client):
    assert client.post("/api/assets", json={}).status_code == 401

def test_validation(client):
    r = client.post("/api/assets", json={"tag": "T-2", "name": "x", "category": "car"}, headers=KEY)
    assert r.status_code == 400 and "category" in r.get_json()["message"]

def test_missing(client):
    assert client.get("/api/assets/NOPE").status_code == 404
