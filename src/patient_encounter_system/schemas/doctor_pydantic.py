from pydantic import BaseModel, PositiveInt
from datetime import datetime
from typing import Optional


class DoctorCreate(BaseModel):
    full_name: str
    specialty: str
    active_status: Optional[bool] = True


class DoctorRead(BaseModel):
    id: PositiveInt
    full_name: str
    specialty: str
    active_status: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
