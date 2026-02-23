from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base   # ✅ IMPORT BASE CHUNG

class User(Base):
    __tablename__ = "users"

    uid = Column(String(128), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
