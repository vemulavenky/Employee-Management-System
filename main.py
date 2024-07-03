from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import Structure, Logics, database

app = FastAPI(title="Employee Information")



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 


#------------------------------DepartMentInfo Endpoints -------------------#
@app.post("/departments/", response_model=Structure.Department, tags=["Department_of_Employee"])
def create_department(department: Structure.DepartmentCreate, db: Session = Depends(get_db)):
    return Logics.create_department(db=db, department=department)

@app.get("/departments/{department_id}", response_model=Structure.Department, tags=["Department_of_Employee"])
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = Logics.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department 

@app.get("/departments/", response_model=list[Structure.Department], tags=["Department_of_Employee"])
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    departments = Logics.get_departments(db, skip=skip, limit=limit)
    return departments 

@app.get("/employees/department/{department_id}", response_model=list[Structure.EmployeeWithDepartment],  tags=["Department_of_Employee"])
def get_employees_with_departments_endpoint(department_id: int, db: Session = Depends(get_db)):
    employees = Logics.get_employees_with_departments(db, department_id)
    
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found for the given department ID")
    
    return employees


#..............EndPoints Of Role_Management.................................................

@app.post("/role/",  tags=["Role_of_Employee"])
def create_role(role:Structure.RoleCreate, db: Session= Depends(get_db)):
    return Logics.create_role(db=db, role=role) 

@app.get("/roles/{role_id}", response_model=Structure.Role, tags=["Role_of_Employee"])
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = Logics.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role




#------------------------- EmployeeInfo EndPoints -------------------#

@app.post("/employees/", response_model=Structure.Employee, tags=["Employee_Information"])
def create_employee(employee: Structure.EmployeeCreate, db: Session = Depends(get_db)):
    return Logics.create_employee(db=db, employee=employee)



@app.get("/employees/{employee_id}", response_model=Structure.Employee, tags=["Employee_Information"])
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = Logics.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.get("/employees/", response_model=list[Structure.Employee], tags=["Employee_Information"])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = Logics.get_employees(db, skip=skip, limit=limit)
    return employees 


@app.put("/employees/{employee_id}", response_model=Structure.Employee, tags=["Employee_Information"])
def update_employee(employee_id: int, employee: Structure.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Logics.update_employee(db=db, employee_id=employee_id, employee_update=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee 


@app.delete("/employees/{employee_id}", tags=["Employee_Information"])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = Logics.delete_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Employee_Info": "Deleted Succesfully"}





##### .........ENDPOINTS FOR ATTENDENCE................############

@app.post("/attendance/", tags=["Attendance"])
def create_attendance_endpoint(Manager_role_id : int, attendance: Structure.AttendanceCreate, db: Session = Depends(get_db)):
    return Logics.create_attendance(db, Manager_role_id , attendance)

@app.get("/attendance/{employee_id}", tags=["Attendance"])
def get_attendance_details_endpoint(employee_id: int, db: Session = Depends(get_db)):
    return Logics.get_attendance_details(db, employee_id)


@app.put("/attendance/{Manager_role_id}/update", tags=["Attendance"])
def update_attendance_endpoint(Manager_role_id: int, attendance_update: Structure.Attendence_Update, db: Session = Depends(get_db)):
    return Logics.update_attendance(db,  Manager_role_id, attendance_update,)




#...........................Endpoints of Leave_Management.......................................................

@app.post("/leave_requests/", tags=["Leave"])
def create_leave_request(leave_request: Structure.LeaveRequestCreate, db: Session = Depends(get_db)):
    return Logics.create_leave_request(db, leave_request)

@app.get("/leave_requests/employee/{employee_id}", response_model=List[Structure.LeaveRequestResponse], tags=["Leave"])
def read_leave_requests_by_employee(employee_id: int, db: Session = Depends(get_db)):
    leave_requests = Logics.get_leave_requests_by_employee(db, employee_id)
    return leave_requests

@app.get("/leave_requests_pending/manager/{manager_id}", response_model=List[Structure.LeaveRequestResponse], tags=["Leave"])
def read_pending_leave_requests_for_manager(manager_id: int, db: Session = Depends(get_db)):
    leave_requests = Logics.get_pending_leave_requests_for_manager(db, manager_id)
    return leave_requests


@app.put("/leave_requests/{leave_request_id}/approve", tags=["Leave"])
def approve_leave_request(leave_request_id: int, approval: Structure.LeaveApproval, db: Session = Depends(get_db)):
    return Logics.approve_leave_request(db, leave_request_id,approval)

StopAsyncIteration