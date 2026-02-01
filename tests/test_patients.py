import pytest
from fastapi.testclient import TestClient
from patient_encounter_system.main import app

@pytest.fixture
def client():
    return TestClient(app)

# ---------- CREATE PATIENT ----------

def test_create_patient_success(client):
    payload = {
        "first_name": "Mark",
        "last_name": "Ruffalo",
        "email": "mark.ruffalo@test.com",
        "phone_number": "7894561230",
    }

    response = client.post("/patients", json=payload)
    assert response.status_code == 201


    data = response.json()
    assert data["first_name"] == "Mark"
    assert data["last_name"] == "Ruffalo"
    assert data["email"] == "mark.ruffalo@test.com"


def test_create_patient_duplicate_email_fails(client):
    payload = {
        "first_name": "Duplicate",
        "last_name": "User",
        "email": "mark.ruffalo@test.com",  # already used
        "phone_number": "8888888888",
    }

    response = client.post("/patients", json=payload)
    assert response.status_code == 400


# ---------- READ PATIENT ----------

def test_read_patient_success(client):
    response = client.get("/patients/1")
    assert response.status_code == 200

    data = response.json()
    assert "first_name" in data
    assert "email" in data


def test_read_patient_not_found(client):
    response = client.get("/patients/9999")
    assert response.status_code == 404


# ---------- LIST PATIENTS ----------

def test_list_patients(client):
    response = client.get("/patients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---------- DELETE PROTECTION ----------

def test_delete_patient_with_appointments_fails(client):
    """
    Patient 1 has appointments (created in appointment tests).
    Deleting must fail.
    """
    response = client.delete("/patients/1")
    assert response.status_code == 409


def test_delete_patient_without_appointments_success(client):
    payload = {
        "first_name": "Temp",
        "last_name": "Patient",
        "email": "temp.patient@test.com",
        "phone_number": "7777777777",
    }

    create_resp = client.post("/patients", json=payload)
    patient_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/patients/{patient_id}")
    assert delete_resp.status_code == 204
