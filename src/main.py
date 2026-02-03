from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from services import (
    patient_service,
    doctor_service,
    appointment_service,
)
from schemas import (
    patient_pydantic,
    doctor_pydantic,
    appointment_pydantic,
)

app = FastAPI(title="Patient Encounter System")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients", response_model=patient_pydantic.PatientRead, status_code=201)
def create_patient(
    patient: patient_pydantic.PatientCreate,
    db: Session = Depends(get_db),
):
    try:
        db_patient = patient_service.create_patient(db, patient)
        return db_patient
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/patients/{patient_id}", response_model=patient_pydantic.PatientRead)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = patient_service.read_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_pydantic.PatientRead(**patient)


@app.get("/patients", response_model=list[patient_pydantic.PatientRead])
def read_all_patients(db: Session = Depends(get_db)):
    patients = patient_service.read_all_patients(db)
    return [patient_pydantic.PatientRead(**p) for p in patients]


@app.post("/doctors", response_model=doctor_pydantic.DoctorRead, status_code=201)
def create_doctor(
    doctor: doctor_pydantic.DoctorCreate,
    db: Session = Depends(get_db),
):
    db_doctor = doctor_service.create_doctor(db, doctor)
    return db_doctor


@app.get("/doctors/{doctor_id}", response_model=doctor_pydantic.DoctorRead)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_service.read_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor_pydantic.DoctorRead(**doctor)


@app.get("/doctors", response_model=list[doctor_pydantic.DoctorRead])
def read_all_doctors(db: Session = Depends(get_db)):
    doctors = doctor_service.read_all_doctors(db)
    return [doctor_pydantic.DoctorRead(**d) for d in doctors]


@app.put(
    "/doctors/{doctor_id}/toggle-status", response_model=doctor_pydantic.DoctorRead
)
def toggle_status_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = doctor_service.toggle_status_doctor(db, doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor


@app.post(
    "/appointments",
    response_model=appointment_pydantic.AppointmentRead,
    status_code=201,
)
def create_appointment(
    appointment: appointment_pydantic.AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        db_appointment = appointment_service.create_appointment(db, appointment)
        return db_appointment
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get(
    "/appointments/by-date", response_model=list[appointment_pydantic.AppointmentRead]
)
def read_appointments_for_a_date(date: str, db: Session = Depends(get_db)):
    appointments = appointment_service.read_appointments_for_a_date(db, date)
    return [appointment_pydantic.AppointmentRead.from_orm(app) for app in appointments]


@app.get(
    "/appointments",
    response_model=list[appointment_pydantic.AppointmentDetailedRead],
)
def list_appointments(
    doctor_id: int | None = None,
    patient_id: int | None = None,
    date: str | None = None,
    db: Session = Depends(get_db),
):
    appointments = appointment_service.list_appointments(
        db, doctor_id, patient_id, date
    )
    return [appointment_pydantic.AppointmentDetailedRead(**a) for a in appointments]


@app.delete("/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        result = patient_service.delete_patient(db, patient_id)
        if not result:
            raise HTTPException(404, "Patient not found")
    except ValueError as e:
        raise HTTPException(409, str(e))


@app.delete("/doctors/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        result = doctor_service.delete_doctor(db, doctor_id)
        if not result:
            raise HTTPException(404, "Doctor not found")
    except ValueError as e:
        raise HTTPException(409, str(e))


@app.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    try:
        result = appointment_service.delete_appointment(db, appointment_id)
        if not result:
            raise HTTPException(404, "Appointment not found")
    except ValueError as e:
        raise HTTPException(409, str(e))
