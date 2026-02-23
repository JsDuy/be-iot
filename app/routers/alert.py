from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert
from app.auth.auth import get_current_user
from app.models.device import Device
from app.models.device_member import DeviceMember

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/")
def get_alerts(
    device_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(404)

    if device.owner_uid != user["uid"]:
        member = db.query(DeviceMember).filter_by(
            device_id=device.id,
            user_uid=user["uid"]
        ).first()
        if not member:
            raise HTTPException(403)

    return (
        db.query(Alert)
        .filter(Alert.device_id == device_id)
        .order_by(Alert.created_at.desc())
        .all()
    )


@router.get("/unread")
def get_unread_alerts(
    device_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 🔐 CHECK QUYỀN (BỎ ĐOẠN BẠN HỎI VÀO ĐÂY)
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(404, "Device not found")

    if device.owner_uid != user["uid"]:
        member = db.query(DeviceMember).filter_by(
            device_id=device.id,
            user_uid=user["uid"]
        ).first()
        if not member:
            raise HTTPException(403, "No permission")

    # ✅ SAU KHI QUA ĐƯỢC CHECK QUYỀN
    return (
        db.query(Alert)
        .filter(Alert.device_id == device_id, Alert.is_read == False)
        .order_by(Alert.created_at.desc())
        .all()
    )

@router.patch("/{alert_id}/read")
def mark_alert_read(
    alert_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(404)

    device = db.query(Device).filter(Device.id == alert.device_id).first()

    if device.owner_uid != user["uid"]:
        member = db.query(DeviceMember).filter_by(
            device_id=device.id,
            user_uid=user["uid"]
        ).first()
        if not member:
            raise HTTPException(403)

    alert.is_read = True
    db.commit()
    return {"status": "ok"}

