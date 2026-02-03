# ruff: noqa: E402
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Doctor(Base):
    """
    Represents a doctor in the hospital.
    """

    __tablename__ = "vamsi_doctors"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    specialty: Mapped[str] = mapped_column(String(100), nullable=False)

    active_status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="1"  # MySQL: 1 = true
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")

    from models.appointment import Appointment
