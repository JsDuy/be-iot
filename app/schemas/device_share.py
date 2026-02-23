from pydantic import BaseModel, EmailStr

class ShareDeviceRequest(BaseModel):
    device_uid: str
    target_email: EmailStr
    role: str = "viewer"

