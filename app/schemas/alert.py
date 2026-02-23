from datetime import datetime
from pydantic import BaseModel

class AlertResponse(BaseModel):
    id: int
    device_id: int
    alert_type: str
    value: float
    threshold: float
    level: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
