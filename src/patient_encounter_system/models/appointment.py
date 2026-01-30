from datetime import datetime
from patient_encounter_system.database import Base
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)



class Appointment(Base):
    """
    Represents an appointment between a patient and a doctor.
    """
    __tablename__ = "vamsi_appointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("vamsi_patients.id"),
        nullable=False
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("vamsi_doctors.id"),
        nullable=False
    )

    appointment_start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    appointment_duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    patient: Mapped["Patient"] = relationship(
    "Patient",
    back_populates="appointments"
    )

    doctor: Mapped["Doctor"] = relationship(
    "Doctor",
    back_populates="appointments"
    )

from patient_encounter_system.models.patient import Patient
from patient_encounter_system.models.doctor import Doctor


