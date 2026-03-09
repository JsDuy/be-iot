from pydantic import BaseModel, Field
from datetime import datetime


class HealthDataResponse(BaseModel):
    heart_rate: int | None
    spo2: int | None
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

    heart_rate: int | None = None
    spo2: int | None = None
    temperature: float | None = None

    gas_level: float | None = None
    humidity: float | None = None
    blood_pressure: str | None = None

    measured_at: datetime | None = None
    is_offline: bool = False

    class Config:
        populate_by_name = True