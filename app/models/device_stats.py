from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class DeviceStats(Base):
    __tablename__ = "device_stats"

    device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    last_seq = Column(Integer, default=0)
    total_packets = Column(Integer, default=0)
    missing_packets = Column(Integer, default=0)
    duplicate_packets = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())