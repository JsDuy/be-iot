from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.health_data import HealthDataCreate
from app.services.alert_service import analyze_and_create_alert
from app.services.realtime_service import push_latest_health
from app.auth.auth import get_current_user
from app.models.health_data import HealthData
from app.schemas.health_data import HealthDataResponse
from app.services.health_pipeline import clean_health_data
from datetime import datetime, timezone
from app.services.seq_monitor import check_seq


router = APIRouter(prefix="/health-data", tags=["Health Data"])



@router.post("/")
def create_health_data(
    data: HealthDataCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1️⃣ Tìm device bằng device_uid
    device = (
        db.query(models.Device)
        .filter(models.Device.device_uid == data.device_uid)
        .first()
    )

    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")


    clean = clean_health_data(
    device.id,
    data.dict()
    )
    check_seq(device.id, data.seq)
    # 2️⃣ Lưu PostgreSQL
    health = models.HealthData(
    device_id=device.id,
    seq=data.seq,               
    heart_rate=clean["heart_rate"],
    spo2=clean["spo2"],
    temperature=clean["temperature"],
    gas_level=data.gas_level,
    humidity=data.humidity,
    blood_pressure=data.blood_pressure,
    measured_at=(
        data.measured_at.replace(tzinfo=None)
        if data.measured_at
        else datetime.utcnow()
    ),
    is_offline=data.is_offline
    )

    db.add(health)
    db.commit()
    db.refresh(health)

    # 3️⃣ Alert
    analyze_and_create_alert(
    db=db,
    device_id=device.id,
    heart_rate=clean["heart_rate"],
    spo2=clean["spo2"],
    temperature=clean["temperature"],
    humidity=data.humidity,
    blood_pressure=data.blood_pressure
)
    

    # 4️⃣ Push realtime Firebase
    push_latest_health(
    device_uid=device.device_uid,
    data={
        "heartRate": clean["heart_rate"],
        "spo2": clean["spo2"],
        "temperature": clean["temperature"],
        "gas": data.gas_level or 0,
        "humidity": data.humidity or 0,
        "bloodPressure": data.blood_pressure or "0/0"
    }
)

    return {"status": "ok"}


@router.get(
    "/by-uid/{device_uid}",
    response_model=list[HealthDataResponse]
)
def get_history_by_uid(
    device_uid: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    device = (
        db.query(models.Device)
        .filter(models.Device.device_uid == device_uid)
        .first()
    )
    if not device:
        raise HTTPException(status_code=404)

    if device.owner_uid != user["uid"]:
        member = db.query(models.DeviceMember).filter_by(
            device_id=device.id,
            user_uid=user["uid"]
        ).first()
        if not member:
            raise HTTPException(status_code=403)

    return (
        db.query(HealthData)
        .filter(HealthData.device_id == device.id)
        .order_by(HealthData.measured_at.desc())
        .limit(200)
        .all()
    )

