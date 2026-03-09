from pydantic import BaseModel

class RevokeDeviceRequest(BaseModel):
    device_uid: str
    target_user_uid: str