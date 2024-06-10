from django.db import models
import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class JobGroup(models.Model):
    JOB=(
        ('Junior Staff','Junior Staff'),
        ('Supervisor','Supervisor'),
        ('Junior Manager','Junior Manager'),
        ('Middle Manager','Middle Manager'),
        ('Senior Manager', 'Senior Manager'),
        ('Intern', 'Intern'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job_group=models.CharField(max_length=50,choices=JOB,default='Junior Staff')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

class Leave(models.Model):
    DEPARTMENT=(
        ('Network','Network & Cloud Development'),
        ('Programming','Programming'),
        ('Cyber security','Cyber Security'),
        ('AI','Artificial Inteligence'),
        ('Finance & Accounts', 'Finance & Accounts'),
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Research & Development', 'Research & Development'),
        ('Customer Support', 'Customer Support'),
        ('Projects Development', 'Projects Development'),
        ('Faculty of Education', 'Faculty of Education'),
        ('Faculty of Science', 'Faculty of Science'),
        ('Faculty of Agriculture', 'Faculty of Agriculture'),
        ('Faculty of Computer Engineering', 'Faculty of Computer Engineering'),
        ('Faculty of Mechanical Engineering', 'Faculty of Mechanical Engineering'),
        ('Faculty of Civil Engineering', 'Faculty of Civil Engineering'),
        ('Faculty of Science & Technology', 'Faculty of Science & Technology'),
        ('Faculty of Law', 'Faculty of Law'),
        ('Faculty of Business Management', 'Faculty of Business Management'),
    )
    STATUS=(
        ('Pending','Pending'),
        ('Declined','Declined'),
        ('Accepted','Accepted'),
    )
    leave_id=models.UUIDField(default=uuid.uuid4)
    department=models.CharField(max_length=50, choices=DEPARTMENT,default='')
    staff=models.ForeignKey(User, on_delete=models.CASCADE)
    reason=models.CharField(max_length=100)
    comment=models.TextField(blank=True)
    start_date=models.DateField()
    end_date=models.DateField()
    status=models.CharField(max_length=20, choices=STATUS ,default='Pending')
    hr_comment=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    posted=models.DateTimeField(default=timezone.now)

 

class Offday(models.Model):
    DEPARTMENT=(
        ('Network','Network & Cloud Development'),
        ('Programming','Programming'),
        ('Cyber security','Cyber Security'),
        ('AI','Artificial Inteligence'),
        ('Finance & Accounts', 'Finance & Accounts'),
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Research & Development', 'Research & Development'),
        ('Customer Support', 'Customer Support'),
        ('Projects Development', 'Projects Development'),
        ('Faculty of Education', 'Faculty of Education'),
        ('Faculty of Science', 'Faculty of Science'),
        ('Faculty of Agriculture', 'Faculty of Agriculture'),
        ('Faculty of Computer Engineering', 'Faculty of Computer Engineering'),
        ('Faculty of Mechanical Engineering', 'Faculty of Mechanical Engineering'),
        ('Faculty of Civil Engineering', 'Faculty of Civil Engineering'),
        ('Faculty of Science & Technology', 'Faculty of Science & Technology'),
        ('Faculty of Law', 'Faculty of Law'),
        ('Faculty of Business Management', 'Faculty of Business Management'),
    )
    STATUS=(
        ('Pending','Pending'),
        ('Declined','Declined'),
        ('Accepted','Accepted'),
    )
    offday_id=models.UUIDField(default=uuid.uuid4)
    department=models.CharField(max_length=50, choices=DEPARTMENT,default='')
    staff=models.ForeignKey(User, on_delete=models.CASCADE)
    reason=models.CharField(max_length=100)
    comment=models.TextField(blank=True)
    start_date=models.DateField()
    end_date=models.DateField()
    status=models.CharField(max_length=20, choices=STATUS ,default='Pending')
    hr_comment=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    posted=models.DateTimeField(default=timezone.now)

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Benefit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=255)
#     national_id = models.CharField(max_length=20)
#     kra_pin = models.CharField(max_length=20)
#     nhif_number = models.CharField(max_length=20)
#     nssf_number = models.CharField(max_length=20)
#     bank_account_number = models.CharField(max_length=50)
#     bank_branch = models.CharField(max_length=100)
#     bank_name = models.CharField(max_length=100)
#     bank_code = models.CharField(max_length=20)
#     bank_address = models.CharField(max_length=255)
#     level_of_education = models.CharField(max_length=255)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     job_group = models.ForeignKey(JobGroup, on_delete=models.CASCADE)
#     benefits = models.ManyToManyField(Benefit)
#     leave_days = models.IntegerField(default=21)
#     off_days = models.IntegerField(default=3)
#     contract_end_date = models.DateField()

#     def __str__(self):
#         return self.full_name
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='human_employee')
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    leave_days = models.IntegerField(default=0)
    off_days = models.IntegerField(default=0)
    benefits = models.ManyToManyField('Benefit')
    job_group = models.CharField(max_length=255)
    contract_renewal_requested = models.BooleanField(default=False)
    contract_renewal_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.full_name

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    # allowances = models.DecimalField(max_digits=10, decimal_places=2)
    paye = models.DecimalField(max_digits=10, decimal_places=2)
    nhif = models.DecimalField(max_digits=10, decimal_places=2)
    nssf = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}"
    
    def send_payslip_email(self):
        subject = f'Payslip for {self.month.strftime("%B, %Y")}'
        html_message = render_to_string('payslip_email.html', {'payslip': self})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = self.employee.user.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    

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

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     failed_login_attempts = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.user.username

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# from django.db.models.signals import post_save
# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)