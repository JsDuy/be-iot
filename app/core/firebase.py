import os
import json
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    """Khởi tạo Firebase Admin SDK một lần duy nhất"""
    if firebase_admin._apps:
        return  # Đã init rồi

    # 1. Ưu tiên: Đọc từ biến môi trường trên Render (FIREBASE_CREDENTIALS = toàn bộ JSON string)
    cred_json_str = os.getenv("FIREBASE_CREDENTIALS")
    database_url = os.getenv("FIREBASE_DATABASE_URL")

    if cred_json_str:
        try:
            cred_dict = json.loads(cred_json_str)
            cred = credentials.Certificate(cred_dict)
            print("Firebase initialized from environment variable FIREBASE_CREDENTIALS")
        except json.JSONDecodeError as e:
            raise ValueError(f"FIREBASE_CREDENTIALS không phải JSON hợp lệ: {e}")
    else:
        # 2. Fallback cho local dev: dùng file firebase_key.json
        BASE_DIR = Path(__file__).resolve().parents[2]
        cred_path = BASE_DIR / "firebase_key.json"

        if cred_path.exists():
            cred = credentials.Certificate(str(cred_path))
            print("Firebase initialized from local file: firebase_key.json")
        else:
            raise FileNotFoundError(
                "Không tìm thấy Firebase credentials. "
                "Trên Render: set biến FIREBASE_CREDENTIALS. "
                "Local: đặt file firebase_key.json ở root dự án."
            )

    # Database URL (nên lấy từ env)
    if not database_url:
        database_url = "https://healthwatch-iot-default-rtdb.asia-southeast1.firebasedatabase.app/"

    firebase_admin.initialize_app(
        cred,
        {"databaseURL": database_url}
    )
    print("Firebase Admin SDK initialized successfully!")

# Gọi init ngay khi import module
initialize_firebase()

# Hàm tiện ích
def get_db_ref(path: str):
    return db.reference(path)