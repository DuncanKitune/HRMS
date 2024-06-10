from django.urls import path
from . import views

urlpatterns = [
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('apply_contract_renewal/', views.apply_contract_renewal, name='apply_contract_renewal'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_employee/', views.create_employee, name='create_employee'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('issue_letter/<int:employee_id>/', views.issue_letter, name='issue_letter'),

    # added on 6/624
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('profile/', views.profile, name='profile'),
    path('add_statutory_deduction/', views.add_statutory_deduction, name='add_statutory_deduction'),

    
]
