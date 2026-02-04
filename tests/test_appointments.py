import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

# -------------------------------------------------
# FORCE ISOLATED TEST DATABASE
# -------------------------------------------------
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from main import app
from database import Base, engine

client = TestClient(app)


# -------------------------------------------------
# DB SETUP
# -------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# -------------------------------------------------
# HELPERS (CREATE DATA PER TEST)
# -------------------------------------------------
def create_patient():
    res = client.post(
        "/patients",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john{datetime.now().timestamp()}@example.com",
            "phone_number": "9999999999",
        },
    )
    assert res.status_code == 201
    return res.json()["id"]


def create_doctor(active=True):
    res = client.post(
        "/doctors",
        json={
            "full_name": "Dr Strange",
            "specialty": "Neurology",
            "active_status": active,
        },
    )
    assert res.status_code == 201
    return res.json()["id"]


def create_appointment(patient_id, doctor_id):
    future_time = datetime.now(timezone.utc) + timedelta(hours=2)

    res = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start_datetime": future_time.isoformat(),
            "appointment_duration_minutes": 30,
        },
    )
    assert res.status_code == 201
    return res.json()["id"]


# -------------------------------------------------
# PATIENT TESTS
# -------------------------------------------------
def test_create_and_get_patient():
    patient_id = create_patient()
    res = client.get(f"/patients/{patient_id}")
    assert res.status_code == 200


# -------------------------------------------------
# DOCTOR TESTS
# -------------------------------------------------
def test_create_doctor():
    doctor_id = create_doctor()
    res = client.get(f"/doctors/{doctor_id}")
    assert res.status_code == 200


def test_toggle_doctor_status():
    doctor_id = create_doctor()
    res = client.put(f"/doctors/{doctor_id}/toggle-status")
    assert res.status_code == 200
    assert res.json()["active_status"] is False


# -------------------------------------------------
# APPOINTMENT TESTS
# -------------------------------------------------
def test_create_appointment():
    patient_id = create_patient()
    doctor_id = create_doctor()
    create_appointment(patient_id, doctor_id)


def test_appointment_overlap_conflict():
    patient_id = create_patient()
    doctor_id = create_doctor()

    create_appointment(patient_id, doctor_id)

    future_time = datetime.now(timezone.utc) + timedelta(hours=2, minutes=10)

    res = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start_datetime": future_time.isoformat(),
            "appointment_duration_minutes": 30,
        },
    )
    assert res.status_code == 409


# -------------------------------------------------
# DELETE CONSTRAINT TESTS
# -------------------------------------------------
def test_delete_doctor_with_appointment_fails():
    patient_id = create_patient()
    doctor_id = create_doctor()
    create_appointment(patient_id, doctor_id)

    res = client.delete(f"/doctors/{doctor_id}")
    assert res.status_code == 409


def test_delete_patient_with_appointment_fails():
    patient_id = create_patient()
    doctor_id = create_doctor()
    create_appointment(patient_id, doctor_id)

    res = client.delete(f"/patients/{patient_id}")
    assert res.status_code == 409





# -----------------------------
# EXTRA TESTS FOR COVERAGE
# -----------------------------

def test_get_patient_not_found():
    res = client.get("/patients/9999")
    assert res.status_code == 404


def test_get_doctor_not_found():
    res = client.get("/doctors/9999")
    assert res.status_code == 404


def test_create_appointment_with_inactive_doctor_fails():
    patient_id = create_patient()
    doctor_id = create_doctor(active=False)

    future_time = datetime.now(timezone.utc) + timedelta(hours=3)

    res = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start_datetime": future_time.isoformat(),
            "appointment_duration_minutes": 30,
        },
    )

    assert res.status_code == 409


def test_list_appointments_by_date():
    patient_id = create_patient()
    doctor_id = create_doctor()
    create_appointment(patient_id, doctor_id)

    today = datetime.now(timezone.utc).date().isoformat()
    res = client.get(f"/appointments?date={today}")

    assert res.status_code == 200


def test_delete_appointment_success():
    patient_id = create_patient()
    doctor_id = create_doctor()
    appointment_id = create_appointment(patient_id, doctor_id)

    res = client.delete(f"/appointments/{appointment_id}")
    assert res.status_code == 204