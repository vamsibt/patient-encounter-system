from sqlalchemy.orm import Session
from sqlalchemy import select, text
from patient_encounter_system.schemas import appointment_pydantic as sch
from patient_encounter_system.models.appointment import Appointment
from datetime import timedelta
from sqlalchemy.sql import func
from patient_encounter_system.models.patient import Patient
from patient_encounter_system.models.doctor import Doctor


def create_appointment(db: Session, appointment: sch.AppointmentCreate):

    new_end = appointment.appointment_start_datetime + timedelta(
        minutes=appointment.appointment_duration_minutes
    )

    stmt = (
    select(Appointment.id)
    .where(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_start_datetime < new_end,
        func.timestampadd(
            text("MINUTE"),
            Appointment.appointment_duration_minutes,
            Appointment.appointment_start_datetime,
        ) > appointment.appointment_start_datetime,
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

def read_all_appointments(db: Session):
    stmt = (
        select(
            # Appointment fields
            Appointment.id.label("appointment_id"),
            Appointment.patient_id.label("appointment_patient_id"),
            Appointment.doctor_id.label("appointment_doctor_id"),
            Appointment.appointment_start_datetime,
            Appointment.appointment_duration_minutes,
            Appointment.created_at,


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
    )

    result = db.execute(stmt).mappings().all()
    return result


def read_appointments_for_doctor_on_date(db: Session, doctor_id: int, date: str):
    stmt = select(
        Appointment.id,
        Appointment.patient_id,
        Appointment.doctor_id,
        Appointment.appointment_start_datetime,
        Appointment.appointment_duration_minutes,
        Appointment.created_at,
    ).where(
        Appointment.doctor_id == doctor_id,
        func.date(Appointment.appointment_start_datetime) == date,
    )

    result = db.execute(stmt).mappings().all()
    return result

def read_appointments_for_a_date(db: Session, date: str):
    stmt = select(
        Appointment.id,
        Appointment.patient_id,
        Appointment.doctor_id,
        Appointment.appointment_start_datetime,
        Appointment.appointment_duration_minutes,
        Appointment.created_at,
    ).where(
        func.date(Appointment.appointment_start_datetime) == date,
    ).order_by(Appointment.appointment_start_datetime)

    result = db.execute(stmt).mappings().all()
    return result
