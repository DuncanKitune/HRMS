from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, Payslip
# from .models import Profile
import logging
from django.core.mail import send_mail
from django.contrib.auth.signals import user_login_failed


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Employee)
def audit_employee_change(sender, instance, created, **kwargs):
    if created:
        action = "Created"
    else:
        action = "Updated"
    logger.info(f"Employee {action}: {instance.full_name}")

@receiver(post_save, sender=Payslip)
def audit_payslip_change(sender, instance, created, **kwargs):
    action = "Created" if created else "Updated"
    logger.info(f"Payslip {action}: {instance.employee.full_name} - {instance.month}")

@receiver(post_save, sender=Payslip)
def send_payslip_on_save(sender, instance, created, **kwargs):
    if created:
        instance.send_payslip_email()

#A signal to automatically create a profile for each user:
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()        



# user_login_failed.connect(check_failed_login)    