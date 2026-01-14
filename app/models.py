from pydantic import BaseModel, Field
from typing import Optional

class AssetBase(BaseModel):
    name: str
    type: str
    status: str = "available"
    assigned_to: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    status: Optional[str]
    assigned_to: Optional[str]

class Asset(AssetBase):
    id: str

class EmployeeBase(BaseModel):
    name: str
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: str