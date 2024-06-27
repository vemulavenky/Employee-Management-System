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

#---------------------------------------DepartMentInfo Endpoints -------------------#
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


@app.post("/role/", response_model=Structure.Role, tags=["Role"])
def create_role(role:Structure.RoleCreate, db: Session= Depends(get_db)):
    return Logics.create_role(db=db, role=role) 

@app.get("/roles/{role_id}", response_model=Structure.Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = Logics.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role 

