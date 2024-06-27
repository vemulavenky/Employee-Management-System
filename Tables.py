from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from database import Base, engine

class Employee_Information(Base):
    __tablename__ = 'EmployeeDeatils' 

    id = Column(Integer, primary_key=True) 
    First_Name = Column(String)
    Last_Name = Column(String) 
    Email = Column(String, unique=True,)
    Phone_Number = Column(String, unique=True) 
    Date_of_Birth = Column(Date) 
    Department_id = Column(Integer, ForeignKey('departments.id')) 
    Role_id = Column(Integer, ForeignKey("roles.id"))
    Date_of_Joined = Column(Date) 
    Is_active = Column(Boolean) 

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    Name_of_Department = Column(String, unique=True)
    description = Column(String)  

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    Name_Of_Role = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)
