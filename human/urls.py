from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    
    # Added on 5/6/24
    path('manage_statutory_deductions/<int:user_id>/', views.manage_statutory_deductions, name='manage_statutory_deductions'),
    path('generate_payslip_pdf/<int:payslip_id>/', views.generate_payslip_pdf, name='generate_payslip_pdf'),
    path('send_payslip_email/<int:payslip_id>/', views.send_payslip_email_view, name='send_payslip_email_view'),
    path('generate_payslips_word/', views.generate_payslips_word, name='generate_payslips_word'),
    path('generate_payslips_excel/', views.generate_payslips_excel, name='generate_payslips_excel'),
    path('generate_statutory_deductions_excel/', views.generate_statutory_deductions_excel, name='generate_statutory_deductions_excel'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
