import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


# ---------- CREATE DOCTOR ----------


def test_create_doctor_success(client):
    payload = {"full_name": "Dr Strange", "specialty": "Magic", "active_status": True}

    response = client.post("/doctors", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["full_name"] == "Dr Strange"
    assert data["specialty"] == "Magic"
    assert data["active_status"] is True

    client.delete(f"/doctors/{data['id']}")


# ---------- READ DOCTOR ----------


def test_read_doctor_success(client):
    response = client.get("/doctors/1")
    assert response.status_code == 200

    data = response.json()
    assert "full_name" in data
    assert "specialty" in data
    assert data["active_status"] is True


def test_read_doctor_not_found(client):
    response = client.get("/doctors/9999")
    assert response.status_code == 404


# ---------- LIST DOCTORS ----------


def test_list_doctors(client):
    response = client.get("/doctors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- TOGGLE STATUS ----------


def test_toggle_doctor_status(client):
    # Initially active
    response = client.get("/doctors/1")
    assert response.json()["active_status"] is True

    # Toggle → inactive
    response = client.put("/doctors/1/toggle-status")
    assert response.status_code == 200
    assert response.json()["active_status"] is False

    # Toggle back → active
    response = client.put("/doctors/1/toggle-status")
    assert response.status_code == 200
    assert response.json()["active_status"] is True


def test_toggle_doctor_not_found(client):
    response = client.put("/doctors/9999/toggle-status")
    assert response.status_code == 404


# ---------- DELETE PROTECTION ----------


def test_delete_doctor_with_appointments_fails(client):
    """
    Doctor 1 already has appointments (created in appointment tests).
    Deleting must fail.
    """
    response = client.delete("/doctors/1")
    assert response.status_code == 409


def test_delete_doctor_without_appointments_success(client):
    # Create new doctor
    payload = {
        "full_name": "Dr Temporary",
        "specialty": "Testing",
    }
    create_resp = client.post("/doctors", json=payload)
    doctor_id = create_resp.json()["id"]

    # Delete should work
    delete_resp = client.delete(f"/doctors/{doctor_id}")
    assert delete_resp.status_code == 204
