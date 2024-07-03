from fastapi import Depends, HTTPException
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

def get_employees_with_departments(db: Session, department_id: int):
    return (
        db.query( 
            Tables.Employee_Information.First_Name, 
            Tables.Employee_Information.Last_Name, 
            Tables.Department.Name_of_Department
        )
        .join(Tables.Department, Tables.Employee_Information.Department_id == Tables.Department.id)
        .filter(Tables.Employee_Information.Department_id == department_id)
        .all()
    )

def create_role(db: Session, role: Structure.Role):
    db_role = Tables.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role 

def get_role(db: Session, role_id: int):
    return db.query(Tables.Role).filter(Tables.Role.id == role_id).first()


def create_attendance(db: Session, Manager_role_id : int, attendance: Structure.AttendanceCreate): 

    employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id ==Manager_role_id).first()
    if not employee_details:
        raise HTTPException(status_code=404, detail="Employee not found")
    role = db.query(Tables.Role).filter(Tables.Role.id == employee_details.Role_id ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.Name_Of_Role not in ["Manager", "IT Manager", "Team Lead"]: 
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

def get_attendance_details(db: Session, employee_id: int):
    employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if not employee_details:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance_details = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id == employee_id).first()
    role = db.query(Tables.Role).filter(Tables.Role.id == employee_details.Role_id).first()

    if attendance_details:
        employee_presence = "Present"
    else:
        employee_presence = "Absent"

    return {
        "id": employee_details.id,
        "First_Name": employee_details.First_Name,
        "Last_name": employee_details.Last_Name,
        "Role": role.Name_Of_Role,
        "attendance_status": employee_presence
    }

def update_attendance(db: Session,  Manager_role_id: int, attendance_update: Structure.Attendence_Update):

    role = db.query(Tables.Role).filter(Tables.Role.id == Manager_role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.Name_Of_Role not in ["Manager", "IT Manager", "Team Lead"]: 
        raise HTTPException(status_code=403, detail="Only Managers, IT Managers, or Team Leads can update attendance")

    employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == attendance_update.employee_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id == employee.id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail=f"No attendance record found for employee '{employee.Last_Name}'")

    attendance.status = attendance_update.status

    db.commit()
    db.refresh(attendance)

    return attendance

def create_leave_request(db: Session, leave_request: Structure.LeaveRequestCreate):
    number_of_days = (leave_request.end_date - leave_request.start_date).days + 1
    db_leave_request = Tables.Leave(
        employee_id=leave_request.employee_id,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status="Pending",
        number_of_days=number_of_days, 
        approver_id =leave_request.approver_id
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

def get_leave_requests_by_employee(db: Session, employee_id: int):
    leave_requests = db.query(Tables.Leave).filter(Tables.Leave.employee_id == employee_id).all()
    return leave_requests


def get_pending_leave_requests_for_manager(db: Session, manager_id: int):
    role = db.query(Tables.Role).filter(Tables.Role.id == manager_id).first() 
    if role.Name_Of_Role not in "IT Manager" :
        raise HTTPException(status_code=404, detail="Manager not found")

    leave_requests = db.query(Tables.Leave).filter(Tables.Leave.approver_id == role.id, Tables.Leave.status == "Pending").all()
    return leave_requests


def approve_leave_request(db: Session, leave_request_id: int, approval: Structure.LeaveApproval):
    leave_request = db.query(Tables.Leave).filter(Tables.Leave.id == leave_request_id).first()

    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    approver = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == leave_request.approver_id).first()
    if not approver:
        raise HTTPException(status_code=404, detail=f"Approver with ID {leave_request.approver_id} not found")
    
    role = db.query(Tables.Role).filter(Tables.Role.id == approver.Role_id).first()

    if role.Name_Of_Role not in ["Manager", "IT Manager", "Team Lead"]:
        raise HTTPException(status_code=403, detail="Only Managers or Team Leads can approve leave requests")
   
    if approval.status == "Approved":
        leave_duration = (leave_request.end_date - leave_request.start_date).days + 1
        employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == leave_request.employee_id).first()
        if employee.Number_of_Leaves < leave_duration:
            raise HTTPException(status_code=400, detail="Insufficient number of leaves available")
        employee.Number_of_Leaves -= leave_duration

        leave_request.status = "Approved"

    elif approval.status == "Rejected":
        leave_request.status = "Rejected" 

    
    db.commit()
    db.refresh(leave_request)
    return leave_request