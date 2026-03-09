from app.core.firebase import get_db_ref
from datetime import datetime

def push_latest_health(device_uid: str, data: dict):
    ref = get_db_ref(f"devices/{device_uid}/health_data/latest")
    clean_data = {k: v for k, v in data.items() if v is not None}
    ref.update(clean_data)

def push_user_device(user_uid: str, device_uid: str, role: str | None):
    ref = get_db_ref(f"users/{user_uid}/devices/{device_uid}")

    if role:
        ref.set({
            "role": role,
            "sharedAt": datetime.utcnow().isoformat()
        })
    else:
        ref.delete()
