from pydantic import BaseModel, PositiveInt
from datetime import datetime
from pydantic import EmailStr

class PatientCreate(BaseModel): 
    first_name : str
    last_name : str
    email: EmailStr
    phone_number: str


class PatientRead(BaseModel):
    id: PositiveInt
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


