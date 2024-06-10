My EA Employee Management System
Overview
The EA Employee Management System (EMS) is a comprehensive web application built with Django for managing employees within an organization. It features user management, employee profiling, leave application processing, contract renewals, and the issuance of various letters and statutory deductions.

Features
User Management
Custom User Model: Extends the default Django user model to include department, job group, date of entry, and contract end date.
User Registration: Admins can create new users with specific roles and permissions.
User Authentication: Secure login and logout functionality.
User Profile: Each user has an associated profile with a photo, date joined, and other personal information.
User Dashboard: Personalized dashboard displaying relevant information and actions for each user.
Employee Management
Employee Profiles: Detailed profiles for each employee, including full name, department, salary, leave days, off days, benefits, and job group.
Inline Employee Editing: Admins can edit employee details directly from the user admin interface.
Leave Management
Leave Application: Employees can apply for leave specifying start date, end date, and reason.
Leave Approval: Leave applications are tracked with statuses such as pending, approved, or rejected.
Contract Management
Contract Renewal: Employees can request contract renewals, which are tracked and managed by the system.
Contract Status: Track and update the status of contract renewal requests.
Document Management
Letters Issuance: Issue various types of letters (e.g., warning, appraisal, recommendation, contract award, contract renewal, and contract end letters) to employees.
Payslips: Generate and manage payslips for employees, including details on basic salary, allowances, deductions, and net pay.
Statutory Deductions
Manage Deductions: Admins can add and manage statutory deductions with names and percentages.

Installation Guide
Prerequisites
Python 3.x
Django 3.x or later
Pillow library for image processing
Database (SQLite is used by default, but PostgreSQL or MySQL can be configured)

Setup
Clone the Repository git clone https://github.com/DuncanKitune/employeemanagementsystem.git cd employeemanagementsystem
Create and Activate Virtual Environment python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
Install Dependencies pip install -r requirements.txt
Database Migrations python manage.py makemigrations python manage.py migrate
Create Superuser python manage.py createsuperuser
Run the Development Server python manage.py runserver
Access the Application Open your web browser and go to http://127.0.0.1:8000/admin to log in with your superuser account.

User Guide
Login
Access the admin interface at /admin. Use the superuser credentials to log in.

Add a New User
Navigate to the "Users" section, click on "Add User", and fill in the required fields.

Edit User Profile
Navigate to the "Users" section, click on the user you want to edit, and modify the details.

Manage Employee Details
Navigate to the "Employees" section, click on an employee to edit details such as department, salary, and job group.

Handle Leave Applications
Navigate to the "Leave Applications" section, review pending leave applications, and update the status to approve or reject.

Process Contract Renewals
Navigate to the "Contract Renewals" section, review pending contract renewal requests, and update the status to approve or reject.

Issue Letters
Navigate to the "Letters" section, click on "Add Letter", fill in the letter details, and associate it with an employee.

Manage Statutory Deductions
Navigate to the "Statutory Deductions" section, click on "Add Deduction", and fill in the deduction details.
Employee Actions

Login
Access the login page at /login. Use your username and password to log in.

View Dashboard
After logging in, you will be redirected to your personalized dashboard.

Apply for Leave
Navigate to the "Apply Leave" section. Fill in the leave application form with start date, end date, and reason. Submit the form.

Request Contract Renewal
Navigate to the "Contract Renewal" section. Fill in the renewal request form with the renewal request date. Submit the form.

View Profile
Navigate to the "Profile" section to view your personal details and update your profile picture if needed.

Project Structure
employeemanagementsystem/
│
├── core/
│   ├── _pycache_
│       ├── __init__.py
│       ├── pyache
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│
├── human/
│    ├── migrations
│       ├── _pycache_
│           ├── _init.py
│           ├── 0001_initial.py
│    ├── __init__.py
│    ├── admin.py
│    ├── apps.py
│    ├── forms.py
│    ├── models.py
│    ├── signals.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
│       
├── media       
│
├── users/
│   ├── migrations
│        ── _pycache_
│           ├── _init.py
│           ├── 0001_initial.py
│   ├── templates/
│       ├── users/
│           ├── dashboard.html
│           ├── login.html
│           ├── add_user.html
│           ├── edit_user.html
│           ├── profile.html
│           ├── apply_leave.html
│           ├── apply_contract_renewal.html
│           ├── issue_letter.html
│           ├── add_statutory_deduction.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── middleware.py
│   ├── modelss.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│
├── db
├── manage.py
├── requirements.txt
├── README.md
├── License