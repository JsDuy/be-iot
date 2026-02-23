from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    # ID phần cứng (ESP32 in sẵn)
    device_code = Column(String(50), unique=True, nullable=False)

    # ID logic trong app
    device_uid = Column(String(100), unique=True, nullable=True)

    device_name = Column(String(100), nullable=True)

    # user sở hữu
    owner_uid = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
