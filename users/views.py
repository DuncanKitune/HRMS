from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from xhtml2pdf import pisa
from docx import Document
from openpyxl import Workbook
from human.models import Department
from .models import CustomUser, Employee, Department, JobGroup, Profile, Payslip, Letter, StatutoryDeduction, LeaveApplication, ContractRenewal
from .forms import CustomUserCreationForm, CustomUserChangeForm, LeaveApplicationForm, ContractRenewalForm, IssueLetterForm, StatutoryDeductionForm, EmployeeCreationForm, EmployeeChangeForm


# homepage added 21/6
def home(request):
    
    return render(request, 'users/homepage.html')
# return HttpResponse("Welcome to the Home Page")
    # if request.user.is_superuser:
    #     return redirect('admin_dashboard')
    # else:
    #     return redirect('employee_dashboard')

# View for logging in
@login_required
def logout_user(request):
    logout(request)
    return redirect('users:login')

@login_required
@permission_required('users.add_customuser', raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully')
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/add_user.html', {'form': form})

@login_required
@permission_required('users.change_customuser', raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('users:dashboard')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('employee_dashboard')  # Redirect to employee dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


# View for logging out
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')  # Redirect to login page after logout


@login_required
def employee_dashboard(request):
    employee = Employee.objects.get(user=request.user)
    leave_days = employee.leave_days
    off_days = employee.off_days
    benefits = employee.benefits.all()
    payslips = Payslip.objects.filter(employee=employee)
    job_group = employee.job_group
    department = employee.department

    current_hour = now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render(request, 'dashboard/employee_dashboard.html', {
        'employee': employee,
        'leave_days': leave_days,
        'off_days': off_days,
        'benefits': benefits,
        'payslips': payslips,
        'greeting': greeting,
        'job_group': job_group,
        'department': department,
    })


@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            reason = form.cleaned_data['reason']
            employee = Employee.objects.get(user=request.user)
            department = employee.department

            # Calculate the number of employees on leave in the same department
            total_employees = Employee.objects.filter(department=department).count()
            concurrent_leaves = LeaveApplication.objects.filter(
                employee__department=department,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status='approved'
            ).count()

            # Calculate the percentage of employees on leave
            leave_percentage = (concurrent_leaves / total_employees) * 100

            if leave_percentage >= 10:
                # Find the next available date when the percentage of employees on leave is below 10%
                proposed_date = end_date + timedelta(days=1)
                while (LeaveApplication.objects.filter(
                    employee__department=department,
                    start_date__lte=proposed_date,
                    end_date__gte=proposed_date,
                    status='approved'
                ).count() / total_employees) * 100 >= 10:
                    proposed_date += timedelta(days=1)

                # Reject the application and inform the user
                form.add_error(None, f'Too many employees are on leave. Try from {proposed_date.strftime("%Y-%m-%d")}.')

                # Optionally send an email notification to the user
                send_mail(
                    'Leave Application Rejected',
                    f'Your leave application from {start_date} to {end_date} has been rejected due to high concurrency. '
                    f'You can reapply from {proposed_date.strftime("%Y-%m-%d")}.',
                    'admin@example.com',
                    [employee.user.email],
                    fail_silently=False,
                )

                return render(request, 'dashboard/apply_leave.html', {'form': form})

            # If leave percentage is below 10%, proceed with the application
            leave_days_taken = (end_date - start_date).days + 1
            if leave_days_taken <= employee.leave_days:
                leave_application = LeaveApplication.objects.create(
                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,
                    reason=reason,
                    status='pending'  # or 'approved' if auto-approval is needed
                )
                employee.leave_days -= leave_days_taken
                employee.save()

                # Send email notification to admin for approval
                send_mail(
                    'Leave Application Submitted',
                    f'{employee.full_name} has applied for leave from {start_date} to {end_date}.\nReason: {reason}',
                    'admin@example.com',
                    ['admin@example.com'],
                    fail_silently=False,
                )

                return redirect('employee_dashboard')
            else:
                form.add_error(None, 'You do not have enough leave days.')
    else:
        form = LeaveApplicationForm()
    return render(request, 'dashboard/apply_leave.html', {'form': form})


@login_required
def apply_contract_renewal(request):
    if request.method == 'POST':
        form = ContractRenewalForm(request.POST)
        if form.is_valid():
            renewal_request_date = form.cleaned_data['renewal_request_date']
            employee = Employee.objects.get(user=request.user)
            # Process contract renewal logic here
            employee.contract_renewal_requested = True
            employee.contract_renewal_date = renewal_request_date
            employee.save()
            # Send email notification to HR or admin about the renewal request
            send_mail(
                'Contract Renewal Request',
                f'{employee.full_name} has requested a contract renewal on {renewal_request_date}.',
                'admin@example.com',
                ['hr@example.com'],
                fail_silently=False,
            )
            return redirect('employee_dashboard')
    else:
        form = ContractRenewalForm()
    return render(request, 'dashboard/apply_contract_renewal.html', {'form': form})


@login_required
def view_payslips(request):
    employee = Employee.objects.get(user=request.user)
    payslips = Payslip.objects.filter(employee=employee)
    return render(request, 'dashboard/view_payslips.html', {'payslips': payslips})


# Admin dashboard view
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    employees = Employee.objects.all()
    leave_applications = LeaveApplication.objects.all()
    contract_renewals = ContractRenewal.objects.all()
    issued_letters = Letter.objects.all()
    payslips = Payslip.objects.all()
    statutory_deductions = StatutoryDeduction.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {
        'employees': employees,
        'leave_applications': leave_applications,
        'contract_renewals': contract_renewals,
        'issued_letters': issued_letters,
        'payslips': payslips,
        'statutory_deductions': statutory_deductions,
    })


# Create employee view
@login_required
def create_employee(request):
   
    if request.method == 'POST':
        # Process employee creation logic here
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        department_id = request.POST.get('department')
        salary = request.POST.get('salary')
        # Create employee object
        department = Department.objects.get(id=department_id)
        # user = .objects.create_user(username=email, email=email, password='defaultpassword')
        employee = Employee.objects.create(
            # user=user,
            full_name=full_name,
            department=department,
            salary=salary,
            # ... other fields
        )
        # Send email to the new employee with activation link
        send_mail(
            'Welcome to the Company',
            f'Hello {full_name},\n\nYou have been added to the company system. Please activate your account and change your default password.\n\nThank you.',
            'admin@example.com',
            [email],
            fail_silently=False,
        )
        return redirect('admin_dashboard')
    departments = Department.objects.all()
    return render(request, 'dashboard/create_employee.html', {'departments': departments})


# Issue letter view
@login_required
def issue_letter(request, employee_id):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = IssueLetterForm(request.POST)
        if form.is_valid():
            letter = Letter(
                type=form.cleaned_data['type'],
                employee=employee,
                subject=form.cleaned_data['subject'],
                content=form.cleaned_data['content']
            )
            letter.save()
            send_mail(
                letter.subject,
                strip_tags(letter.content),
                settings.EMAIL_HOST_USER,
                [employee.user.email],
                html_message=letter.content,
                fail_silently=False,
            )
            return redirect('admin_dashboard')
    else:
        form = IssueLetterForm()
    return render(request, 'dashboard/issue_letter.html', {'employee': employee, 'form': form})


# Function to send payslip email
def send_payslip_email(payslip):
    subject = f'Payslip for {payslip.month.strftime("%B, %Y")}'
    html_message = render_to_string('payslip_email.html', {'payslip': payslip})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = payslip.employee.user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


# Generate payslip PDF
@login_required
def generate_payslip_pdf(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)
    template_path = 'payslip.html'
    context = {'payslip': payslip}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payslip.month.strftime("%B_%Y")}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# Send payslip email view
@login_required
@permission_required('users.send_email', raise_exception=True)
def send_payslip_email_view(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)
    send_payslip_email(payslip)
    return HttpResponse('Payslip sent successfully!')

# added on 6/6
@login_required
@permission_required('users.add_statutorydeduction', raise_exception=True)
def add_statutory_deduction(request):
    if request.method == 'POST':
        form = StatutoryDeductionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statutory deduction added successfully')
            return redirect('users:dashboard')
    else:
        form = StatutoryDeductionForm()
    return render(request, 'users/add_statutory_deduction.html', {'form': form})

#added 21/6
# Transfer Employee
@login_required
@permission_required('users.change_department', raise_exception=True)
def transfer_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        new_department_id = request.POST.get('new_department')
        new_department = Department.objects.get(id=new_department_id)
        employee.department = new_department
        employee.save()
        messages.success(request, f'{employee.full_name} transferred to {new_department.name} successfully.')
        return redirect('admin_dashboard')
    departments = Department.objects.all()
    return render(request, 'transfer_employee.html', {'employee': employee, 'departments': departments})

# Account Activation Email
@login_required
@permission_required('users.add_customuser', raise_exception=True)
def account_activation_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        subject = 'Activate Your Account'
        template = render_to_string('account_activation_email.html', {'user': user})
        plain_message = strip_tags(template)
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email])
        messages.success(request, 'Account activation email sent successfully!')
        return redirect('admin_dashboard')
    return render(request, 'account_activation_email.html', {'user': user})

# Alter Employee Benefits
@login_required
@permission_required('users.change_employee', raise_exception=True)
def alter_employee_benefits(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeChangeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'{employee.full_name} benefits altered successfully.')
            return redirect('admin_dashboard')
    else:
        form = EmployeeChangeForm(instance=employee)
    return render(request, 'alter_employee_benefits.html', {'form': form})

# Approve Leave
@login_required
@permission_required('users.change_leaveapplication', raise_exception=True)
def approve_leave(request, leave_id):
    leave_application = get_object_or_404(LeaveApplication, id=leave_id)
    if request.method == 'POST':
        leave_application.status = 'Approved'
        leave_application.save()
        messages.success(request, 'Leave application approved successfully!')
        return redirect('admin_dashboard')
    return render(request, 'approve_leave.html', {'leave_application': leave_application})

# Generate Report
@login_required
@permission_required('users.view_report', raise_exception=True)
def generate_report(request):
    # Implement report generation logic here
    return render(request, 'generate_report.html') 