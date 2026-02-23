from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from sqlalchemy.orm import Session

from app.database import get_db, upsert_user

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        # 1️⃣ Verify Firebase ID Token
        decoded = firebase_auth.verify_id_token(credentials.credentials)

        uid = decoded["uid"]
        email = decoded.get("email")

        # 2️⃣ AUTO UPSERT USER → PostgreSQL
        if email:
            upsert_user(db, uid, email)

        # 3️⃣ Trả user cho các router dùng
        return {
            "uid": uid,
            "email": email,
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
        )
