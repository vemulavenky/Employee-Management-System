from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import Structure, Logics, database,Tables

app = FastAPI(title="Employee Information")



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 


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

#---------------------------------End Of Employee Infoo------------------------------------------------------------

#---------------------------EndPoint Of Employee with Deaprtment-----------------------------
@app.get("/employees/with-departments/{department_id}", response_model=list[Structure.EmployeeWithDepartment])
def read_employees_with_departments(department_id:int, db: Session = Depends(get_db)):
    employees_with_departments = Logics.get_employees_with_departments(db,department_id)
    if not employees_with_departments:
        raise HTTPException(status_code=404, detail="No employees found")
    return employees_with_departments

#------------------------------DepartMentInfo Endpoints -------------------#
@app.post("/departments/", response_model=Structure.Department, tags=["Department"])
def create_department(department: Structure.DepartmentCreate, db: Session = Depends(get_db)):
    return Logics.create_department(db=db, department=department)

@app.get("/departments/{department_id}", response_model=Structure.Department, tags=["Department"])
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = Logics.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department 

@app.get("/departments/", response_model=list[Structure.Department], tags=["Department"])
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    departments = Logics.get_departments(db, skip=skip, limit=limit)
    return departments
#-----------------------End Of the Department Deatails----------------------- 


@app.post("/role/",  tags=["Role"])
def create_role(role:Structure.RoleCreate, db: Session= Depends(get_db)):
    return Logics.create_role(db=db, role=role) 

@app.get("/roles/{role_id}", response_model=Structure.Role, tags=["Role"])
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = Logics.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@app.post("/attendance/", tags=["Attendence"])
def create_attendance(attendance: Structure.AttendanceCreate, db: Session = Depends(get_db)):

    role = db.query(Tables.Role).filter(Tables.Role.Name_Of_Role == attendance.role_name).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.Name_Of_Role not in ["Manager", "IT Manager", "Team Lead"]:  # Add any other managerial roles here
        raise HTTPException(status_code=403, detail="Only Managers or Team Leads can mark attendance")
    new_attendance = Tables.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance 
@app.get("/attendence/{employee_id}", tags=["Attendence"]) 
def get_attendence_details(employee_id : int, db:Session=Depends(get_db)):
    employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if not employee_details:
        raise HTTPException(status_code=404, detail="Employee not found")
    attendence_details = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id ==employee_id).first() 
    role = db.query(Tables.Role).filter(Tables.Role.id == employee_details.Role_id).first()

    if attendence_details :
        employee_presence = "Present" 
    else :
        employee_presence = "Absent" 

    return {
        "id": employee_details.id,
        "First_Name": employee_details.First_Name,
        "Last_name": employee_details.Last_Name,
        "Role" : role.Name_Of_Role,
        "attendance_status": employee_presence 
    } 

@app.put("/attendence/{employee_id}/update", tags=["Attendence"]) 
def updation_attendence(employee_id : int , attendence_update: Structure.Attendence_Update, db: Session = Depends(get_db)): 

    employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first() 

    if not employee:
         raise HTTPException(status_code=404, detail="Employee not found") 
    
    attendence = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id == employee.id).first() 

    if not attendence:
        raise HTTPException(status_code=404, detail=f"No attendance record found for employee '{employee.Last_Name}'") 
    
    attendence.status = attendence_update.status 

    db.commit()
    db.refresh(attendence) 

    return attendence