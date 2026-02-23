from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class HealthDataResponse(BaseModel):
    heart_rate: int
    spo2: int
    temperature: float | None
    gas_level: float | None
    humidity: float | None          
    blood_pressure: str | None
    measured_at: datetime

    class Config:
        from_attributes = True
class HealthDataCreate(BaseModel):
    device_uid: str  
    seq: int | None = None             
    heart_rate: int
    spo2: int
    temperature: Optional[float] = None
    gas_level: float | None = None
    humidity: float | None = None          
    blood_pressure: str | None = None 

    measured_at: datetime | None = None
    is_offline: bool = False