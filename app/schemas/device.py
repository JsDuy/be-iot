from pydantic import BaseModel

class DeviceRegisterRequest(BaseModel):
    device_code: str      # ESP32_01
    device_uid: str       # D0123
    device_name: str

class Device(BaseModel):
    id: int
    device_code: str
    device_uid: str | None
    device_name: str | None

    class Config:
        from_attributes = True
