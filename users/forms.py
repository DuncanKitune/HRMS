from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LeaveApplication, ContractRenewal, Letter, StatutoryDeduction, CustomUser, Employee, Department, JobGroup

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'department', 'job_group', 'date_of_entry', 'contract_end_date', "is_staff", "is_active")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'department', 'job_group', 'date_of_entry', 'contract_end_date', "is_staff", "is_active")

class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model =Employee
        fields = ('user', 'full_name', 'department', 'salary', 'leave_days', 'off_days', 'benefits', 'job_group') 

class EmployeeChangeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('user', 'full_name', 'department', 'salary', 'leave_days', 'off_days', 'benefits', 'job_group')   

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description') 

class JobGroupForm(forms.ModelForm):
    class Meta:
        model = JobGroup 
        fields = ('name',)             

# Created before 6/6
class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class ContractRenewalForm(forms.ModelForm):
    class Meta:
        model = ContractRenewal
        fields = ['renewal_request_date']
        widgets = {
            'renewal_request_date': forms.TextInput(attrs={'type': 'date'}),
        }

# Added 5/6/24
class IssueLetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['type', 'subject', 'content']

class StatutoryDeductionForm(forms.ModelForm):
    class Meta:
        model = StatutoryDeduction
        fields = ['name', 'percentage']


# # class UserRegistrationForm(UserCreationForm):
#     class Meta:
#           model = CustomUser
#           fields = ['first_name', 'last_name', 'email', 'telephone_number', 'date_of_birt']         