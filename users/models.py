from django.db import models
from django.conf import settings
from PIL import Image

# Create your models here.
from django.contrib.auth.models import AbstractUser, User,Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid
# Create your models here.
from django.contrib.auth import get_user_model
CustomUser=get_user_model()
from human.models import Department, Benefit, JobGroup


   
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to="profile", default='avatar.jpg')
    date_joined=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user.username    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.photo.path)
        if img.height > 300 or img.width > 300 :
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

            #Added on 5/6/24
class StatutoryDeduction(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class LeaveApplication(models.Model):
    employee = models.ForeignKey('users.Employee', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.employee.full_name} - {self.start_date} to {self.end_date}"

class ContractRenewal(models.Model):
    employee = models.ForeignKey('users.Employee', on_delete=models.CASCADE)
    renewal_request_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.employee.full_name} - {self.renewal_request_date}"

# Added on 5/6/24
class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_employee')
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    leave_days = models.IntegerField(default=21)
    off_days = models.IntegerField(default=3)
    benefits = models.ManyToManyField('Benefit')
    job_group = models.CharField(max_length=255)
    contract_renewal_requested = models.BooleanField(default=False)
    contract_renewal_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.full_name

class Letter(models.Model):
    TYPE_CHOICES = [
        ('warning', 'Warning Letter'),
        ('appraisal', 'Appraisal Letter'),
        ('recommendation', 'Recommendation Letter'),
        ('contract_award', 'Contract Award Letter'),
        ('contract_renewal', 'Contract Renewal Letter'),
        ('contract_end', 'Contract End Letter'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.employee.user.username}"

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee.user.username} - {self.month.strftime('%B, %Y')}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Benefit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# added 6/6
class JobGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
            
class CustomUser(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    job_group = models.ForeignKey(JobGroup, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_entry = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')


