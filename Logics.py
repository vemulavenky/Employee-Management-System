from sqlalchemy.orm import Session
import Tables, Structure



def get_employee(db: Session, employee_id: int):
    return db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tables.Employee_Information).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: Structure.Employee):
    db_employee = Tables.Employee_Information(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee 

def update_employee(db: Session, employee_id: int, employee_update: Structure.EmployeeCreate):
    db_employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if db_employee:
        
        if db.query(Tables.Department).filter(Tables.Department.id == employee_update.Department_id).first() is None:
            raise ValueError(f"Department with id {employee_update.Department_id} does not exist")
        
        if db.query(Tables.Role).filter(Tables.Role.id == employee_update.Role_id).first() is None:
            raise ValueError(f"Role with id {employee_update.Role_id} does not exist")

        db_employee.First_Name = employee_update.First_Name
        db_employee.Last_Name = employee_update.Last_Name
        db_employee.Email = employee_update.Email
        db_employee.Phone_Number = employee_update.Phone_Number
        db_employee.Date_of_Birth = employee_update.Date_of_Birth
        db_employee.Department_id = employee_update.Department_id
        db_employee.Role_id = employee_update.Role_id
        db_employee.Date_of_Joined = employee_update.Date_of_Joined
        db_employee.Is_active = employee_update.Is_active
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee



def get_employees_with_departments(db: Session, department_id: int):
    return (
        db.query(Tables.Employee_Information.First_Name, Tables.Employee_Information.Last_Name, Tables.Department.Name_of_Department)
        .join(Tables.Department, Tables.Employee_Information.Department_id == department_id)
        .all()
    )


def get_department(db: Session, department_id: int):
    return db.query(Tables.Department).filter(Tables.Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tables.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: Structure.Department):
    db_department = Tables.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department 

def get_employees_by_department(db: Session, department_id: int):
    return db.query(Tables.Employee_Information).filter(Tables.Employee_Information.Department_id == department_id).all() 


def create_role(db: Session, role: Structure.Role):
    db_role = Tables.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role 

def get_role(db: Session, role_id: int):
    return db.query(Tables.Role).filter(Tables.Role.id == role_id).first()
