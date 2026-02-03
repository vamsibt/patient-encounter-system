from pydantic import BaseModel, field_validator, computed_field, PositiveInt
from datetime import datetime, timezone, timedelta


class AppointmentCreate(BaseModel):
    patient_id: PositiveInt
    doctor_id: PositiveInt
    appointment_start_datetime: datetime
    appointment_duration_minutes: int

    @field_validator("appointment_start_datetime")
    @classmethod
    def must_be_timezone_aware(cls, value: datetime):
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("appointment_start_datetime must be timezone-aware")

        now = datetime.now(timezone.utc)
        if value <= now:
            raise ValueError("appointment_start_datetime must be in the future")

        return value

    @field_validator("appointment_duration_minutes")
    @classmethod
    def duration_must_be_valid(cls, value: int):
        if value < 15 or value > 180:
            raise ValueError("appointment_duration_minutes must be between 15 and 180")
        return value


class AppointmentRead(BaseModel):
    id: PositiveInt
    patient_id: PositiveInt
    doctor_id: PositiveInt
    appointment_start_datetime: datetime
    appointment_duration_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True

    @computed_field
    def appointment_end_datetime(self) -> datetime:
        return self.appointment_start_datetime + timedelta(
            minutes=self.appointment_duration_minutes
        )


class AppointmentDetailedRead(BaseModel):
    appointment_id: PositiveInt
    appointment_start_datetime: datetime
    appointment_duration_minutes: int
    created_at: datetime

    patient_id: PositiveInt
    patient_first_name: str
    patient_last_name: str
    patient_email: str

    doctor_id: PositiveInt
    doctor_full_name: str
    doctor_specialty: str

    class Config:
        from_attributes = True

    @computed_field
    def appointment_end_datetime(self) -> datetime:
        return self.appointment_start_datetime + timedelta(
            minutes=self.appointment_duration_minutes
        )
