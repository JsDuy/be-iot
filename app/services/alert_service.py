from app.models.alert import Alert

def analyze_and_create_alert(
    db,
    device_id,
    heart_rate=None,
    spo2=None,
    temperature=None,
    humidity=None,
    blood_pressure=None
):
    # ❤️ HEART RATE
    if heart_rate is not None:
        if heart_rate >= 120:
            db.add(Alert(
                device_id=device_id,
                alert_type="HEART_RATE",
                value=heart_rate,
                threshold=120,
                level="DANGER",
                message="Nhịp tim quá cao"
            ))
        elif heart_rate >= 100:
            db.add(Alert(
                device_id=device_id,
                alert_type="HEART_RATE",
                value=heart_rate,
                threshold=100,
                level="WARNING",
                message="Nhịp tim cao"
            ))

    # 🫁 SPO2
    if spo2 is not None and spo2 <= 90:
        db.add(Alert(
            device_id=device_id,
            alert_type="SPO2",
            value=spo2,
            threshold=90,
            level="DANGER",
            message="SpO2 thấp"
        ))

    # 🌡️ TEMPERATURE
    if temperature is not None:
        if temperature >= 39:
            db.add(Alert(
                device_id=device_id,
                alert_type="TEMP",
                value=temperature,
                threshold=39,
                level="DANGER",
                message="Nhiệt độ cơ thể rất cao"
            ))
        elif temperature >= 37.5:
            db.add(Alert(
                device_id=device_id,
                alert_type="TEMP",
                value=temperature,
                threshold=37.5,
                level="WARNING",
                message="Nhiệt độ cơ thể cao"
            ))