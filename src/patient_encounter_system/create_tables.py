# ruff: noqa: F401

from patient_encounter_system.database import engine
from patient_encounter_system.database import Base

# IMPORTANT: import all models so SQLAlchemy knows them
from patient_encounter_system.models.patient import Patient
from patient_encounter_system.models.doctor import Doctor
from patient_encounter_system.models.appointment import Appointment


def create_tables():
    Base.metadata.create_all(bind=engine)
    print(" Tables created successfully")


if __name__ == "__main__":
    create_tables()
