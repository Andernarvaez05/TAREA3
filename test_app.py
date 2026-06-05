import json
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200

def test_listar(client):
    r = client.get("/api/students")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_agregar(client):
    r = client.post("/api/students",
                    data=json.dumps({"name": "Test", "grade": 8.0, "career": "Sistemas"}),
                    content_type="application/json")
    assert r.status_code == 201

def test_nota_invalida(client):
    r = client.post("/api/students",
                    data=json.dumps({"name": "X", "grade": 15.0, "career": "Y"}),
                    content_type="application/json")
    assert r.status_code == 400