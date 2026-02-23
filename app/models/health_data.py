from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Boolean, BigInteger
from sqlalchemy.sql import func
from app.database import Base

class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False
    )

    seq = Column(BigInteger, nullable=True)   
    heart_rate = Column(Integer, nullable=True)
    spo2 = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)
    gas_level = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)          
    blood_pressure = Column(String, nullable=True)

    measured_at = Column(DateTime, nullable=True)
    is_offline = Column(Boolean, default=False)

    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False   
    )
