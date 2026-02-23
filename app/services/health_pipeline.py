# app/services/health_pipeline.py
import math

from app.core.data_cleaning.missing import fill_missing
from app.core.data_cleaning.outlier import remove_outlier
from app.core.data_cleaning.noise_filter import MovingAverageFilter

DEVICE_STATE = {}

def get_device_state(device_id: int):
    if device_id not in DEVICE_STATE:
        DEVICE_STATE[device_id] = {
            "last_hr": 80,
            "last_spo2": 98,
            "last_temp": 36.8,
            "hr_filter": MovingAverageFilter(5),
            "spo2_filter": MovingAverageFilter(5),
            "temp_filter": MovingAverageFilter(5),
        }
    return DEVICE_STATE[device_id]


def clean_health_data(device_id: int, payload: dict):
    state = get_device_state(device_id)

    # HR / SpO2 giữ nguyên
    hr = fill_missing(payload.get("heart_rate"), state["last_hr"])
    spo2 = fill_missing(payload.get("spo2"), state["last_spo2"])

    # 🌡️ TEMP: KHÔNG ĐƯỢC BỊA
    raw_temp = payload.get("temperature")

    if raw_temp is None or raw_temp <= 0:
        temp = None   # ✅ mất dữ liệu thật
    else:
        temp = raw_temp
        temp = state["temp_filter"].filter(temp)
        temp = remove_outlier(temp, 34, 40, None)
        state["last_temp"] = temp   # chỉ update khi hợp lệ

    # Update HR / SpO2 state
    state["last_hr"] = hr
    state["last_spo2"] = spo2

    return {
        "heart_rate": round(hr),
        "spo2": round(spo2),
        "temperature": round(temp, 2) if temp is not None else None
    }

