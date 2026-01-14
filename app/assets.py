from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Asset, AssetCreate, AssetUpdate
from app.database import db
from bson import ObjectId

# Create a router for asset-related endpoints
router = APIRouter(prefix="/assets", tags=["assets"])

# Helper function to convert MongoDB asset document to a dictionary
def asset_helper(asset) -> dict:
    return {
        "id": str(asset["_id"]),
        "name": asset["name"],
        "type": asset["type"],
        "status": asset["status"],
        "assigned_to": asset.get("assigned_to"),
    }

# Endpoint to create a new asset
@router.post("/", response_model=Asset)
async def create_asset(asset: AssetCreate):
    result = await db.assets.insert_one(asset.dict())  # Insert asset into DB
    new_asset = await db.assets.find_one({"_id": result.inserted_id})  # Retrieve the inserted asset
    return asset_helper(new_asset)

# Endpoint to list all assets (up to 100)
@router.get("/", response_model=List[Asset])
async def list_assets():
    assets = await db.assets.find().to_list(100)  # Get up to 100 assets
    return [asset_helper(a) for a in assets]

# Endpoint to get a single asset by its ID
@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_helper(asset)

# Endpoint to update an asset by its ID
@router.put("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, asset: AssetUpdate):
    update_data = {k: v for k, v in asset.dict().items() if v is not None}  # Only update provided fields
    await db.assets.update_one({"_id": ObjectId(asset_id)}, {"$set": update_data})
    updated = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_helper(updated)

# Endpoint to delete an asset by its ID
@router.delete("/{asset_id}")
async def delete_asset(asset_id: str):
    result = await db.assets.delete_one({"_id": ObjectId(asset_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted"}

# Endpoint to assign an asset to an employee
@router.post("/{asset_id}/assign/{employee_id}")
async def assign_asset(asset_id: str, employee_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    await db.assets.update_one(
        {"_id": ObjectId(asset_id)},
        {"$set": {"assigned_to": employee_id, "status": "assigned"}}
    )
    return {"message": "Asset assigned"}

# Endpoint to unassign an asset (make it available)
@router.post("/{asset_id}/unassign")
async def unassign_asset(asset_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    await db.assets.update_one(
        {"_id": ObjectId(asset_id)},
        {"$set": {"assigned_to": None, "status": "available"}}
    )
    return {"message": "Asset unassigned"}