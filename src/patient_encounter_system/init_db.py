from patient_encounter_system.database import engine, Base

# IMPORTANT: import models
from patient_encounter_system.models.patient import Patient
from patient_encounter_system.models.doctor import Doctor
from patient_encounter_system.models.appointment import Appointment


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
