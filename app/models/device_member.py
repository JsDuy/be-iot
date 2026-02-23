from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy import UniqueConstraint

class DeviceMember(Base):
    __tablename__ = "device_members"
    __table_args__ = (
        UniqueConstraint("device_id", "user_uid", name="uq_device_member"),
    )

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"))
    user_uid = Column(String(128), nullable=False)
    role = Column(String(20), default="viewer")
    created_at = Column(DateTime, server_default=func.now())
