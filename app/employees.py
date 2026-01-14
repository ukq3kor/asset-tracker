from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Employee, EmployeeCreate
from app.database import db
from bson import ObjectId

router = APIRouter(prefix="/employees", tags=["employees"])

def employee_helper(emp) -> dict:
    return {
        "id": str(emp["_id"]),
        "name": emp["name"],
        "department": emp["department"],
    }

@router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    result = await db.employees.insert_one(employee.dict())
    new_emp = await db.employees.find_one({"_id": result.inserted_id})
    return employee_helper(new_emp)

@router.get("/", response_model=List[Employee])
async def list_employees():
    emps = await db.employees.find().to_list(100)
    return [employee_helper(e) for e in emps]

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    emp = await db.employees.find_one({"_id": ObjectId(employee_id)})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(emp)

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    result = await db.employees.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}