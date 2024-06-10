from django.contrib import admin

# Register your models here.
from.models import JobGroup, Leave, Offday, Department, Benefit, Employee, Payslip

admin.site.register(JobGroup)
admin.site.register(Leave)
admin.site.register(Offday)
admin.site.register(Department)
admin.site.register(Benefit)
admin.site.register(Employee)
admin.site.register(Payslip)
# admin.site.register(Letter)