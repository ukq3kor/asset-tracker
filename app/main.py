# Import FastAPI framework
from fastapi import FastAPI

# Import routers from assets and employees modules
from app.assets import router as asset_router
from app.employees import router as employee_router

# Create FastAPI application instance with a title
app = FastAPI(title="Asset Tracking API")

# Include the asset router to handle asset-related endpoints
app.include_router(asset_router)

# Include the employee router to handle employee-related endpoints
app.include_router(employee_router)