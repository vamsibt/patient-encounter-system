from tracemalloc import start
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from schemas import appointment_pydantic as sch
from models.appointment import Appointment
from datetime import timedelta, timezone
from sqlalchemy.sql import func
from models.patient import Patient
from models.doctor import Doctor


def create_appointment(db: Session, appointment: sch.AppointmentCreate):

    get_patient = db.get(Patient, appointment.patient_id)

    if not get_patient:
        raise ValueError("Patient not found")

    # check doctor exists
    get_doctor = db.get(Doctor, appointment.doctor_id)
    if not get_doctor:
        raise ValueError("Doctor not found")

    if not get_doctor.active_status:
        raise ValueError("Doctor is inactive and cannot accept appointments")

    start = appointment.appointment_start_datetime
    if start.tzinfo is not None:
        start = start.astimezone(timezone.utc).replace(tzinfo=None)

    new_end = start + timedelta(minutes=appointment.appointment_duration_minutes)

    existing_appointments = (
        db.query(Appointment)
        .filter(Appointment.doctor_id == appointment.doctor_id)
        .all()
    )

    for appt in existing_appointments:
        appt_start = appt.appointment_start_datetime
        appt_end = appt_start + timedelta(minutes=appt.appointment_duration_minutes)

        if start < appt_end and new_end > appt_start:
            raise ValueError("Doctor already has an overlapping appointment")

    stmt = (
        select(Appointment.id)
        .where(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_start_datetime < new_end,
            func.timestampadd(
                text("MINUTE"),
                Appointment.appointment_duration_minutes,
                Appointment.appointment_start_datetime,
            )
            > appointment.appointment_start_datetime,
        )
        .limit(1)
    )

    overlap = db.execute(stmt).scalar_one_or_none()
    if overlap:
        raise ValueError("Doctor already has an overlapping appointment")

    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_start_datetime=appointment.appointment_start_datetime,
        appointment_duration_minutes=appointment.appointment_duration_minutes,
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def read_appointment(db: Session, appointment_id: int):
    stmt = (
        select(
            # Appointment fields
            Appointment.id.label("appointment_id"),
            Appointment.appointment_start_datetime,
            Appointment.appointment_duration_minutes,
            # Patient fields
            Patient.id.label("patient_id"),
            Patient.first_name.label("patient_first_name"),
            Patient.last_name.label("patient_last_name"),
            Patient.email.label("patient_email"),
            # Doctor fields
            Doctor.id.label("doctor_id"),
            Doctor.full_name.label("doctor_full_name"),
            Doctor.specialty.label("doctor_specialty"),
        )
        .join(Patient, Patient.id == Appointment.patient_id)
        .join(Doctor, Doctor.id == Appointment.doctor_id)
        .where(Appointment.id == appointment_id)
    )

    result = db.execute(stmt).mappings().one_or_none()
    return result


def list_appointments(
    db: Session,
    doctor_id: int | None = None,
    patient_id: int | None = None,
    date: str | None = None,
):
    stmt = (
        select(
            Appointment.id.label("appointment_id"),
            Appointment.appointment_start_datetime,
            Appointment.appointment_duration_minutes,
            Appointment.created_at,
            Patient.id.label("patient_id"),
            Patient.first_name.label("patient_first_name"),
            Patient.last_name.label("patient_last_name"),
            Patient.email.label("patient_email"),
            Doctor.id.label("doctor_id"),
            Doctor.full_name.label("doctor_full_name"),
            Doctor.specialty.label("doctor_specialty"),
        )
        .join(Patient)
        .join(Doctor)
    )

    if doctor_id:
        stmt = stmt.where(Appointment.doctor_id == doctor_id)

    if patient_id:
        stmt = stmt.where(Appointment.patient_id == patient_id)

    if date:
        stmt = stmt.where(func.date(Appointment.appointment_start_datetime) == date)

    return db.execute(stmt).mappings().all()


def delete_appointment(db: Session, appointment_id: int):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        return False

    db.delete(appointment)
    db.commit()
    return True
