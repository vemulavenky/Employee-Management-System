from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr 

class EmployeeBase(BaseModel):
    First_Name: str
    Last_Name: str
    Email: EmailStr
    Phone_Number: str
    Date_of_Birth: date
    Department_id: int
    Role_id : int
    Date_of_Joined: date
    Is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id : int 

    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    Name_of_Department: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    Name_of_Department: Optional[str]
    description: Optional[str]

class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeWithDepartment(BaseModel):
    First_Name: str
    Last_Name: str
    Name_of_Department: str 
    Name_of_Role : str

class RoleBase(BaseModel):
     Name_Of_Role: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: str

class AttendanceCreate(AttendanceBase):
    role_name:str 

class Attendence_Update(BaseModel):
    employee_id: int
    date: date
    status: str

class Attendance(AttendanceBase):
    id: int
    class Config:
        from_attributes = True
