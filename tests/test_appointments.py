import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_appointment_success(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 3,
        "appointment_start_datetime": "2026-04-30T12:00:00Z",
        "appointment_duration_minutes": 60,
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 201
    client.delete(f"/appointments/{response.json()['id']}")


def test_appointment_conflict(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 4,
        "appointment_start_datetime": "2026-02-10T10:00:00Z",
        "appointment_duration_minutes": 60,
    }

    res = client.post("/appointments", json=payload)

    conflict_payload = {
        "patient_id": 1,
        "doctor_id": 4,
        "appointment_start_datetime": "2026-02-10T10:30:00Z",
        "appointment_duration_minutes": 30,
    }

    response = client.post("/appointments", json=conflict_payload)
    assert response.status_code == 409
    client.delete(f"/appointments/{res.json()['id']}")


def test_appointment_in_past(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_start_datetime": "2020-01-01T10:00:00Z",
        "appointment_duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 422


def test_inactive_doctor_cannot_accept_appointment(client):
    client.put("/doctors/1/toggle-status")  # deactivate

    payload = {
        "patient_id": 1,
        "doctor_id": 1,
        "appointment_start_datetime": "2026-02-11T10:00:00Z",
        "appointment_duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)

    client.put("/doctors/1/toggle-status")
    # print(response.status_code)
    assert response.status_code == 409


def test_create_appointment_doctor_not_found(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 9999,
        "appointment_start_datetime": "2026-05-01T10:00:00Z",
        "appointment_duration_minutes": 30,
    }

    response = client.post("/appointments", json=payload)
    assert response.status_code == 409
    assert "Doctor not found" in response.text


def test_list_appointments(client):
    response = client.get("/appointments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_appointments_by_doctor(client):
    response = client.get("/appointments?doctor_id=3")
    assert response.status_code == 200


def test_list_appointments_by_date(client):
    response = client.get("/appointments?date=2026-06-01")
    assert response.status_code == 200


def test_delete_appointment_success(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 3,
        "appointment_start_datetime": "2026-07-01T10:00:00Z",
        "appointment_duration_minutes": 30,
    }

    create = client.post("/appointments", json=payload)
    appointment_id = create.json()["id"]

    response = client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 204


def test_delete_appointment_not_found(client):
    response = client.delete("/appointments/99999")
    assert response.status_code == 404
