from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Employee, EmployeeCreate
from app.database import db
from bson import ObjectId

# Create a router for employee-related endpoints
router = APIRouter(prefix="/employees", tags=["employees"])

# Helper function to convert MongoDB document to dictionary
def employee_helper(emp) -> dict:
    return {
        "id": str(emp["_id"]),  # Convert ObjectId to string
        "name": emp["name"],
        "department": emp["department"],
    }

# Endpoint to create a new employee
@router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    # Insert the new employee into the database
    result = await db.employees.insert_one(employee.dict())
    # Retrieve the newly created employee document
    new_emp = await db.employees.find_one({"_id": result.inserted_id})
    # Return the employee data in the expected format
    return employee_helper(new_emp)

# Endpoint to list all employees (up to 100)
@router.get("/", response_model=List[Employee])
async def list_employees():
    # Fetch up to 100 employee documents from the database
    emps = await db.employees.find().to_list(100)
    # Convert each document to the expected dictionary format
    return [employee_helper(e) for e in emps]

# Endpoint to get a single employee by ID
@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    # Find the employee document by ObjectId
    emp = await db.employees.find_one({"_id": ObjectId(employee_id)})
    if not emp:
        # Raise 404 if employee not found
        raise HTTPException(status_code=404, detail="Employee not found")
    # Return the employee data
    return employee_helper(emp)

# Endpoint to delete an employee by ID
@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    # Attempt to delete the employee document by ObjectId
    result = await db.employees.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        # Raise 404 if no document was deleted
        raise HTTPException(status_code=404, detail="Employee not found")
    # Return a success message
    return {"message": "Employee deleted"}