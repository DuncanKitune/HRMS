from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
User=get_user_model()
from .models import Profile
from django.dispatch import receiver
from django.contrib.auth.signals import user_login_failed
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()        

@receiver(user_login_failed)
def check_failed_login(sender, credentials, request, **kwargs):
    try:
        user = User.objects.get(username=credentials.get('username'))
        profile = user.profile
        profile.failed_login_attempts += 1
        profile.save()
        if profile.failed_login_attempts >= 5:
            user.is_active = False
            user.save()
            send_mail(
                'Account Locked',
                'Your account has been locked due to multiple failed login attempts.',
                'admin@example.com',
                [user.email],
                fail_silently=False,
            )
    except User.DoesNotExist:
        pass    