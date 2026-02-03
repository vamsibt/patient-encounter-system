# ruff: noqa: F401

from src.database import engine
from src.database import Base

# IMPORTANT: import all models so SQLAlchemy knows them
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment


def create_tables():
    Base.metadata.create_all(bind=engine)
    print(" Tables created successfully")


if __name__ == "__main__":
    create_tables()
