# Employee Management System

The Employee Management System is a Python script that demonstrates the use of SQLAlchemy, a popular Object Relational Mapping (ORM) library, to manage employee data in a SQLite database. This script defines three main classes: Employee, Department, and Project, and establishes relationships between them. It allows you to perform various operations such as adding, removing, and promoting employees, as well as displaying employee information. Additionally, it handles many-to-many relationships between employees and projects.

# Table of Contents
- Employee Management System
- Description
- Table of Contents
- Installation
- Usage
- Functionality
- Contributing
- License

# Add Employees to the Database
This functionality allows you to add employees to the database with the following details:

First name
Last name
Position
Salary
Years of experience
Department
When you choose to add an employee, the system will prompt you to provide these details. It will then create an Employee object and add it to the database. The employee's information will be associated with the specified department. For example:

bash
Copy code
Added Ian Gichachi to the ICT department.

# Remove Employees from the Database by ID
You can remove employees from the database by specifying their unique ID. When you choose to remove an employee, the system will prompt you to enter the ID of the employee you want to remove. It will then delete the employee record from the database. For example:

bash
Copy code
Removed Ian Gichachi from the database.

# Promote Employees by ID
This functionality allows you to promote employees by specifying their unique ID. You can update their position and salary. When you choose to promote an employee, the system will prompt you to enter the ID of the employee you want to promote, as well as the new position and salary. It will then update the employee's information in the database. For example:

bash
Copy code
Ian Gichachi has been promoted to Manager with a salary of $120000.

# Display a List of All Employees
You can display a list of all employees in the database along with their details. When you choose to display employees, the system will retrieve all employee records from the database and print their full name, position, salary, years of experience, and department. For example:

bash
Copy code
Ian Gichachi is a Manager with a salary of $120000, 5 years of experience, in the ICT department.
Mercy Murithi is an Accountant with a salary of $75000, 3 years of experience, in the Accounting department.
...
# Handle Many-to-Many Relationships Between Employees and Projects
The system can handle many-to-many relationships between employees and projects. This means that an employee can be assigned to multiple projects, and a project can have multiple employees working on it. The script includes the necessary database tables and associations to manage these relationships.

# Detect and Remove Duplicate Employee Records
The script includes a function to detect and remove duplicate employee records based on first name, last name, and department. When you run the remove_duplicates function, it will identify employees with the same first name, last name, and department and remove all but one of the duplicates. This helps maintain data integrity in the database.