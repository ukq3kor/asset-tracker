from fastapi import FastAPI
from app.assets import router as asset_router
from app.employees import router as employee_router

app = FastAPI(title="Asset Tracking API")

app.include_router(asset_router)
app.include_router(employee_router)