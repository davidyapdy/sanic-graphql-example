from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationships

from database import Base


# Basic SQLAlchemy
class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    department = relationships(
        Department,
        backref=backref('employee',
                        uselist=True,
                        cascade='delete,all'))
    role = relationships(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))
