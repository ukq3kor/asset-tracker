from pydantic import BaseModel, Field
from typing import Optional

# Base schema for Asset with common fields
class AssetBase(BaseModel):
    name: str  # Name of the asset
    type: str  # Type/category of the asset
    status: str = "available"  # Status of the asset, default is "available"
    assigned_to: Optional[str] = None  # Employee ID or name the asset is assigned to

# Schema for creating a new Asset, inherits all fields from AssetBase
class AssetCreate(AssetBase):
    pass

# Schema for updating an Asset, all fields are optional
class AssetUpdate(BaseModel):
    name: Optional[str]  # Optional updated name
    type: Optional[str]  # Optional updated type
    status: Optional[str]  # Optional updated status
    assigned_to: Optional[str]  # Optional updated assignment

# Schema representing an Asset with an ID
class Asset(AssetBase):
    id: str  # Unique identifier for the asset

# Base schema for Employee with common fields
class EmployeeBase(BaseModel):
    name: str  # Name of the employee
    department: str  # Department the employee belongs to

# Schema for creating a new Employee, inherits all fields from EmployeeBase
class EmployeeCreate(EmployeeBase):
    pass

# Schema representing an Employee with an ID
class Employee(EmployeeBase):
    id: str  # Unique identifier for the employee