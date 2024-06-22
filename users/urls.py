from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('apply_contract_renewal/', views.apply_contract_renewal, name='apply_contract_renewal'),
    
    
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('issue_letter/<int:employee_id>/', views.issue_letter, name='issue_letter'),

    # added on 6/624
    path('profile/', views.profile, name='profile'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    
    path('add_statutory_deduction/', views.add_statutory_deduction, name='add_statutory_deduction'),

#added 21/6
    path('', views.home, name='user_home'),  # Example URL pattern for users app
    path('payslip_email/', views.send_payslip_email, name='payslip_email'),
    path('transfer_employee/', views.transfer_employee, name='transfer_employee'),
    path('account_activation_email/', views.account_activation_email, name='account_activation_email'),
    # path('account_activation_invalid/', views.account_activation_invalid, name='account_activation_invalid'),
    path('alter_employee_benefits/', views.alter_employee_benefits, name='alter_employee_benefits'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('generate_report/', views.generate_report, name='generate_report'),
   
]
   

