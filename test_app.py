import json
import pytest
import app as app_module
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def reset_students():
    """Restaura la lista original entre cada test."""
    original = [s.copy() for s in app_module.STUDENTS]
    original_id = app_module._next_id
    yield
    app_module.STUDENTS.clear()
    app_module.STUDENTS.extend(original)
    app_module._next_id = original_id


# ── Test 1 ────────────────────────────────────────────────────────────────────
def test_home_carga(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"EduTrack" in r.data


# ── Test 2 ────────────────────────────────────────────────────────────────────
def test_listar_estudiantes(client):
    r = client.get("/api/students")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


# ── Test 3 ────────────────────────────────────────────────────────────────────
def test_agregar_estudiante(client):
    r = client.post("/api/students",
                    data=json.dumps({"name": "Test User", "grade": 8.0, "career": "Sistemas"}),
                    content_type="application/json")
    assert r.status_code == 201
    d = r.get_json()
    assert d["name"] == "Test User"
    assert d["grade"] == 8.0


# ── Test 4 ────────────────────────────────────────────────────────────────────
def test_nota_invalida(client):
    r = client.post("/api/students",
                    data=json.dumps({"name": "X", "grade": 15.0, "career": "Y"}),
                    content_type="application/json")
    assert r.status_code == 400


# ── Test 5 ────────────────────────────────────────────────────────────────────
def test_nombre_vacio(client):
    r = client.post("/api/students",
                    data=json.dumps({"name": "", "grade": 7.0, "career": "Z"}),
                    content_type="application/json")
    assert r.status_code == 400


# ── Test 6 ────────────────────────────────────────────────────────────────────
def test_eliminar_estudiante(client):
    r = client.delete("/api/students/1")
    assert r.status_code == 200
    assert r.get_json().get("ok") is True


# ── Test 7 ────────────────────────────────────────────────────────────────────
def test_eliminar_inexistente(client):
    r = client.delete("/api/students/9999")
    assert r.status_code == 404


# ── Test 8 ────────────────────────────────────────────────────────────────────
def test_busqueda(client):
    r = client.get("/api/students?q=ana")
    assert r.status_code == 200
    for s in r.get_json():
        assert "ana" in s["name"].lower()