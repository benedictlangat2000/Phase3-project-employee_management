import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from employee_management import Employee, Department, Project

# Database engine
engine = create_engine('sqlite:///employee_management.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """Employee Management System CLI"""

@cli.command()
@click.argument('first_name')
@click.argument('last_name')
@click.argument('position')
@click.argument('salary', type=int)
@click.argument('years', type=int)
@click.argument('department_name')
def add_employee(first_name, last_name, position, salary, years, department_name):
    """Add an employee to a department"""
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
        click.echo(f"Added {employee.full_name()} to the {department_name} department.")
    else:
        click.echo(f"Department {department_name} does not exist. Employee not added.")

@cli.command()
@click.argument('employee_id', type=int)
def remove_employee(employee_id):
    """Remove an employee by ID"""
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        click.echo(f"Removed {employee.full_name()} from the database.")
    else:
        click.echo(f"Employee with ID {employee_id} not found. No action taken.")

@cli.command()
@click.argument('employee_id', type=int)
@click.argument('new_position')
@click.argument('new_salary', type=int)
def promote_employee(employee_id, new_position, new_salary):
    """Promote an employee by ID"""
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        employee.position = new_position
        employee.salary = new_salary
        session.commit()
        click.echo(f"{employee.full_name()} has been promoted to {new_position} with a salary of ${new_salary}.")
    else:
        click.echo(f"Employee with ID {employee_id} not found. Promotion not applied.")

@cli.command()
def display_employees():
    """Display all employees"""
    employees = session.query(Employee).all()
    for employee in employees:
        click.echo(f"{employee.full_name()} is a {employee.position} with a salary of ${employee.salary}, {employee.years} years of experience, in the {employee.department.name} department.")

if __name__ == "__main__":
    cli()
@cli.command()
def main_menu():
    """Main menu for the Employee Management System"""
    while True:
        click.echo("\nEmployee Management System Menu:")
        click.echo("1. Add Employee")
        click.echo("2. Remove Employee")
        click.echo("3. Promote Employee")
        click.echo("4. Display Employees")
        click.echo("5. Quit")

        choice = click.prompt("Enter your choice (1/2/3/4/5)", type=int)

        if choice == 1:
            add_employee()
        elif choice == 2:
            remove_employee()
        elif choice == 3:
            promote_employee()
        elif choice == 4:
            display_employees()
        elif choice == 5:
            click.echo("Exiting the program.")
            break
        else:
            click.echo("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    cli()