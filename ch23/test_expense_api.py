import os
os.environ["EXPENSE_DB"] = "test_expenses.db"
if os.path.exists("test_expenses.db"):
    os.remove("test_expenses.db")

from fastapi.testclient import TestClient
from expense_api import app

client = TestClient(app)


def test_create_and_read():
    r = client.post("/expenses", json={"spent_on": "2026-10-05", "category": "food",
                                       "description": "Groceries", "amount": 1250.50})
    assert r.status_code == 201
    new_id = r.json()["id"]
    assert client.get(f"/expenses/{new_id}").json()["description"] == "Groceries"


def test_validation_errors():
    r = client.post("/expenses", json={"category": "pets", "description": "", "amount": -5})
    assert r.status_code == 422
    fields = {e["loc"][-1] for e in r.json()["detail"]}
    assert fields == {"category", "description", "amount"}


def test_summary_and_filters():
    client.post("/expenses", json={"spent_on": "2026-10-07", "category": "transport",
                                   "description": "Fuel", "amount": 2000})
    s = client.get("/summary/2026-10").json()
    assert s["total"] == 3250.5 and s["by_category"]["transport"] == 2000
    assert len(client.get("/expenses", params={"category": "food"}).json()) == 1
    assert client.get("/expenses", params={"month": "Oct"}).status_code == 422


def test_delete_and_404():
    new_id = client.post("/expenses", json={"category": "other", "description": "x", "amount": 1}).json()["id"]
    assert client.delete(f"/expenses/{new_id}").status_code == 204
    assert client.get(f"/expenses/{new_id}").status_code == 404
