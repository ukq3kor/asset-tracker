from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Asset, AssetCreate, AssetUpdate
from app.database import db
from bson import ObjectId

router = APIRouter(prefix="/assets", tags=["assets"])

def asset_helper(asset) -> dict:
    return {
        "id": str(asset["_id"]),
        "name": asset["name"],
        "type": asset["type"],
        "status": asset["status"],
        "assigned_to": asset.get("assigned_to"),
    }

@router.post("/", response_model=Asset)
async def create_asset(asset: AssetCreate):
    result = await db.assets.insert_one(asset.dict())
    new_asset = await db.assets.find_one({"_id": result.inserted_id})
    return asset_helper(new_asset)

@router.get("/", response_model=List[Asset])
async def list_assets():
    assets = await db.assets.find().to_list(100)
    return [asset_helper(a) for a in assets]

@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_helper(asset)

@router.put("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, asset: AssetUpdate):
    update_data = {k: v for k, v in asset.dict().items() if v is not None}
    await db.assets.update_one({"_id": ObjectId(asset_id)}, {"$set": update_data})
    updated = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset_helper(updated)

@router.delete("/{asset_id}")
async def delete_asset(asset_id: str):
    result = await db.assets.delete_one({"_id": ObjectId(asset_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted"}

@router.post("/{asset_id}/assign/{employee_id}")
async def assign_asset(asset_id: str, employee_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    await db.assets.update_one({"_id": ObjectId(asset_id)}, {"$set": {"assigned_to": employee_id, "status": "assigned"}})
    return {"message": "Asset assigned"}

@router.post("/{asset_id}/unassign")
async def unassign_asset(asset_id: str):
    asset = await db.assets.find_one({"_id": ObjectId(asset_id)})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    await db.assets.update_one({"_id": ObjectId(asset_id)}, {"$set": {"assigned_to": None, "status": "available"}})
    return {"message": "Asset unassigned"}