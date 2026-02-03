# ruff: noqa: F401

from src.database import engine
from src.database import Base

# IMPORTANT: import all models so SQLAlchemy knows them
<<<<<<< HEAD
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment
=======
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
>>>>>>> b0d2e738c694bf08cef7735fc227ce14ba611813


def create_tables():
    Base.metadata.create_all(bind=engine)
    print(" Tables created successfully")


if __name__ == "__main__":
    create_tables()
