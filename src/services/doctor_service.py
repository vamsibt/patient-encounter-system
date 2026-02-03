from sqlalchemy.orm import Session
from src.models import doctor as models
from schemas import doctor_pydantic as sch
from sqlalchemy import select
from sqlalchemy.sql import func
from models.appointment import Appointment
from models.doctor import Doctor


def create_doctor(db: Session, doctor: sch.DoctorCreate):
    db_doctor = models.Doctor(
        full_name=doctor.full_name,
        specialty=doctor.specialty,
        active_status=doctor.active_status,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def read_doctor(db: Session, doctor_id: int):
    stmt = select(
        models.Doctor.id,
        models.Doctor.full_name,
        models.Doctor.specialty,
        models.Doctor.active_status,
        models.Doctor.created_at,
        models.Doctor.updated_at,
    ).where(models.Doctor.id == doctor_id)

    result = db.execute(stmt).mappings().one_or_none()
    return result


def read_all_doctors(db: Session):
    stmt = select(
        models.Doctor.id,
        models.Doctor.full_name,
        models.Doctor.specialty,
        models.Doctor.active_status,
        models.Doctor.created_at,
        models.Doctor.updated_at,
    )

    result = db.execute(stmt).mappings().all()
    return result


def toggle_status_doctor(db: Session, doctor_id: int):
    db_doctor = db.get(models.Doctor, doctor_id)
    if not db_doctor:
        return None
    if db_doctor.active_status:
        db_doctor.active_status = False
    else:
        db_doctor.active_status = True
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        return None

    has_appointments = db.scalar(
        select(func.count())
        .select_from(Appointment)
        .where(Appointment.doctor_id == doctor_id)
    )

    if has_appointments > 0:
        raise ValueError("Doctor has appointments and cannot be deleted")

    db.delete(doctor)
    db.commit()
    return doctor
