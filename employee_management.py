#!/usr/bin/python3
# Import necessary libraries
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

# Create a base class for declarative models
Base = declarative_base()

# Define the association table for the many-to-many relationship
employee_projects = Table('employee_projects', Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)

# Define the Employee class
class Employee(Base):
    # Specify the table name
    __tablename__ = 'employees'

    # Define columns and their data types
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    salary = Column(Integer)
    years = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Create a relationship to the Department model (one-to-many - employees in departments)
    department = relationship("Department", back_populates="employees")

    # Create a relationship to the Project model (many-to-many - employees assigned to projects)
    projects = relationship("Project", secondary=employee_projects)

    # Defining a method to get the full name of an employee
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Define the Department class
class Department(Base):
    # Specify the table name
    __tablename__ = 'departments'

    # Define columns and their data types
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Create a relationship to the Employee model
    employees = relationship("Employee", back_populates="department")

# Define the Project class
class Project(Base):
    __tablename__ = 'projects'

    # Define columns and their data types
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Create a relationship to the Employee model
    employees = relationship("Employee", secondary=employee_projects)

# Create the database and tables
engine = create_engine('sqlite:///employee_management.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# methods to create employees
# Function to add an employee to a department
def add_employee(first_name, last_name, position, salary, years, department_name):
    department = session.query(Department).filter_by(name=department_name).first()
    if department:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            position=position,
            salary=salary,
            years=years,
            department=department
        )
        session.add(employee)
        session.commit()
        print(f"Added {employee.full_name()} to the {department_name} department.")
    else:
        print(f"Department {department_name} does not exist. Employee not added.")

# methods to remove employees
# Function to remove an employee by ID
def remove_employee(employee_id):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        print(f"Removed {employee.full_name()} from the database.")
    else:
        print(f"Employee with ID {employee_id} not found. No action taken.")

# Function to promote an employee by ID
def promote_employee(employee_id, new_position, new_salary):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        employee.position = new_position
        employee.salary = new_salary
        session.commit()
        print(f"{employee.full_name()} has been promoted to {new_position} with a salary of ${new_salary}.")
    else:
        print(f"Employee with ID {employee_id} not found. Promotion not applied.")

# Function to display all employees
def display_employees():
    employees = session.query(Employee).all()
    for employee in employees:
        print(f"{employee.full_name()} is a {employee.position} with a salary of ${employee.salary}, {employee.years} years of experience, in the {employee.department.name} department.")

# Add departments to the database
department1 = Department(name='ICT')
department2 = Department(name='Accounting')
department3 = Department(name='Management')
department4 = Department(name='Human Resource')
department5 = Department(name='Evaluation')
department6 = Department(name='Tours')

# Add employees to the database
employee1 = Employee(first_name='Ian', last_name='Gichachi', position='ICT', salary=100000, years=5, department=department1)
employee2 = Employee(first_name='Mercy', last_name='Murithi', position='Accountant', salary=75000, years=3, department=department2)
employee3 = Employee(first_name='Benedict', last_name='Langat', position='Manager', salary=150000, years=10, department=department3)
employee4 = Employee(first_name='Sharon', last_name='Asaja', position='Human Resource', salary=120000, years=6, department=department4)
employee5 = Employee(first_name='Jennifer', last_name='Mwendwa', position='Evaluation', salary=50000, years=4, department=department5)
employee6 = Employee(first_name='Davison', last_name='Brian', position='Tours', salary=80000, years=2, department=department6)



project1 = Project(name='Project A')
project2 = Project(name='Project B')
project3 = Project(name='Project C')

# Add employees to the session
session.add(employee1)
session.add(employee2)
session.add(employee3)
session.add(employee4)
session.add(project1)
session.add(project2)
session.add(project3)

# Assign employees to projects
employee1.projects.append(project1)
employee2.projects.append(project1)
employee2.projects.append(project2)
employee3.projects.append(project3)

# Commit the changes to the database
session.commit()

# Query the database for all employees
employees = session.query(Employee).all()

# Print the full name, position, salary, years of experience, and department for each employee
for employee in employees:
    print(f"{employee.full_name()} is a {employee.position} with a salary of ${employee.salary}, {employee.years} years of experience, in the {employee.department.name} department.")

    
# Function to remove duplicates from the Employee table
def remove_duplicates():
    # Query for employees with the same first_name, last_name, and department
    duplicate_employees = session.query(Employee).join(Department).group_by(Employee.first_name, Employee.last_name, Employee.department_id).having(func.count().label('count') > 1).all()

    for duplicate_employee in duplicate_employees:
        print(f"Found duplicate employee: {duplicate_employee.full_name()} in the {duplicate_employee.department.name} department. Removing duplicates...")

        # Get all duplicate entries for the employee
        duplicate_entries = session.query(Employee).filter_by(
            first_name=duplicate_employee.first_name,
            last_name=duplicate_employee.last_name,
            department_id=duplicate_employee.department_id
        ).all()

        # Keep the first occurrence of the duplicate and remove the rest
        if len(duplicate_entries) > 1:
            for entry in duplicate_entries[1:]:
                session.delete(entry)

    session.commit()

# Call the remove_duplicates function to remove duplicates and update the database
remove_duplicates()
