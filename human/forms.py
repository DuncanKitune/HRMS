from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Benefit, Payslip, Letter, Department, JobGroup, StatutoryDeduction
from django.forms import modelformset_factory

class IssueLetterForm(forms.Form):
    letter_type = forms.ChoiceField(choices=Letter.TYPE_CHOICES, label='Letter Type')
    subject = forms.CharField(max_length=100, label='Subject')
    content = forms.CharField(widget=forms.Textarea, label='Content')

class EmployeeCreationForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(label='Email')
    national_id = forms.CharField(max_length=20, label='National ID/Passport Number')
    kra_pin = forms.CharField(max_length=20, label='KRA PIN')
    nhif_number = forms.CharField(max_length=20, label='NHIF Number')
    nssf_number = forms.CharField(max_length=20, label='NSSF Number')
    bank_account_number = forms.CharField(max_length=30, label='Bank Account Number')
    bank_name = forms.CharField(max_length=100, label='Bank Name')
    bank_branch = forms.CharField(max_length=100, label='Bank Branch')
    bank_code = forms.CharField(max_length=10, label='Bank Code')
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label='Department')
    job_group = forms.ModelChoiceField(queryset=JobGroup.objects.all(), label='Job Group')
    salary = forms.DecimalField(max_digits=10, decimal_places=2, label='Salary')
    benefits = forms.ModelMultipleChoiceField(queryset=Benefit.objects.all(), label='Benefits', required=False)

StatutoryDeductionFormSet = modelformset_factory(
    StatutoryDeduction,
    fields=('name', 'percentage'),
    extra=0,
)    