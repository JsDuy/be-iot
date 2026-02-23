from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Device, HealthData
from app.services.alert_service import analyze_and_create_alert
from app.services.realtime_service import push_latest_health
from app.schemas.iot import EspHealthPayload
from app.services.health_pipeline import clean_health_data
from datetime import datetime, timezone

router = APIRouter(prefix="/iot", tags=["IoT"])

@router.post("/push")
def esp_push_data(payload: EspHealthPayload, db: Session = Depends(get_db)):

    device = db.query(Device).filter(
        Device.device_code == payload.device_code
    ).first()

    if not device:
        raise HTTPException(404)

    clean = clean_health_data(
        device.id,
        payload.dict()
    )

    health = HealthData(
    device_id=device.id,
    seq=payload.seq,
    heart_rate=clean["heart_rate"],
    spo2=clean["spo2"],
    temperature=clean["temperature"],
    gas_level=payload.gas_level,
    humidity=payload.humidity,
    blood_pressure=payload.blood_pressure,
    measured_at=(
        payload.measured_at.replace(tzinfo=None)
        if payload.measured_at
        else datetime.utcnow()
    ),
    is_offline=payload.is_offline
    )

    db.add(health)

    analyze_and_create_alert(
        db,
        device.id,
        clean["heart_rate"],
        clean["spo2"],
        clean["temperature"],
        payload.humidity,
        payload.blood_pressure
    )

    db.commit()

    push_latest_health(
    device_uid=device.device_uid,
    data={
        "heartRate": clean["heart_rate"],
        "spo2": clean["spo2"],
        "temperature": clean["temperature"],
        "gas": payload.gas_level,
        "humidity": payload.humidity,
        "bloodPressure": payload.blood_pressure
    }
)

    return {"status": "ok"}