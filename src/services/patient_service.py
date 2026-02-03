from sqlalchemy.orm import Session
from src.models import patient as models
from sqlalchemy import select
from schemas import patient_pydantic as sch
from sqlalchemy.sql import func
from models.appointment import Appointment
from models.patient import Patient


def create_patient(db: Session, patient: sch.PatientCreate):
    db_patient = models.Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        email=patient.email,
        phone_number=patient.phone_number,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def read_patient(db: Session, patient_id: int):
    stmt = select(
        models.Patient.id,
        models.Patient.first_name,
        models.Patient.last_name,
        models.Patient.email,
        models.Patient.phone_number,
        models.Patient.created_at,
        models.Patient.updated_at,
    ).where(models.Patient.id == patient_id)

    result = db.execute(stmt).mappings().one_or_none()
    return result


def read_all_patients(db: Session):
    stmt = select(
        models.Patient.id,
        models.Patient.first_name,
        models.Patient.last_name,
        models.Patient.email,
        models.Patient.phone_number,
        models.Patient.created_at,
        models.Patient.updated_at,
    )
    result = db.execute(stmt).mappings().all()
    return result


def delete_patient(db: Session, patient_id: int):
    patient = db.get(Patient, patient_id)
    if not patient:
        return None

    has_appointments = db.scalar(
        select(func.count())
        .select_from(Appointment)
        .where(Appointment.patient_id == patient_id)
    )

    if has_appointments > 0:
        raise ValueError("Patient has appointments and cannot be deleted")

    db.delete(patient)
    db.commit()
    return patient
