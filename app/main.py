from fastapi import FastAPI
from app.database import Base, engine

from app.routers.device import router as device_router
from app.routers.health_data import router as health_data_router
from app.routers.alert import router as alert_router
from app.routers.iot import router as iot_router

import app.core.firebase  # init Firebase

app = FastAPI(
    title="Health Monitor API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(device_router)
app.include_router(health_data_router)
app.include_router(alert_router)
app.include_router(iot_router)

@app.get("/")
def root():
    return {"status": "API Server is running"}
