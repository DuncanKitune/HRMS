# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Profile, CustomUser, Employee, Department, JobGroup, User
# from .forms import CustomUserCreationForm, CustomUserChangeForm, EmployeeCreationForm, EmployeeChangeForm

# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = 'Employees'
#     fk_name = 'user'
#     # form = EmployeeChangeForm

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     inlines = (EmployeeInline)
#     list_display = ("email", "is_staff", "is_active",)
#     list_filter = ("email", "is_staff", "is_active",)
#     fieldsets = (
#         (None, {"fields": ("username", "email", "password")}),
#         ("Personal info", {"fields": ("first_name", "last_name")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": (
#                 "username", "email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions",
#             ),
#         }),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Department)
# admin.site.register(JobGroup)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["user", "photo", "date_joined"]

# # Register Employee separately if it needs to be independently managed.
# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ("user", "full_name", "department", "salary", "leave_days", "off_days", "job_group")

# # Added 20/6/24
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False

# class CustomUserAdmin(UserAdmin):
#     inlines = [ProfileInline]

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# # from django.contrib import admin
# # from django.contrib.auth.admin import UserAdmin
# # from django.db import models
# # from django.contrib.auth.models import Group, Permission
# # from django.utils.translation import gettext_lazy as _
# # from .models import Profile, CustomUser, Employee, Department, JobGroup
# # # Register your models here.
# # from .forms import CustomUserCreationForm, CustomUserChangeForm, EmployeeCreationForm, EmployeeChangeForm


# # class EmployeeInline(admin.StackedInline):
# #     model = Employee
# #     can_delete = False
# #     verbose_name_plural = 'Employees'
# #     fk_name = 'user'
# #     form = EmployeeChangeForm


# # class CustomUserAdmin(UserAdmin):
# #     add_form = CustomUserCreationForm
# #     form = CustomUserChangeForm
# #     model = CustomUser
# #     inlines = (EmployeeInline,)
# #     list_display = ("email", "is_staff", "is_active",)
# #     list_filter = ("email", "is_staff", "is_active",)
# #     fieldsets = (
# #         (None, {"fields": ("email", "password")}),
# #         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
# #     )
# #     add_fieldsets = (
# #         (None, {
# #             "classes": ("wide",),
# #             "fields": (
# #                 "email", "username", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions",
# #             ),
# #         }),
# #     )
# #     search_fields = ("email",)
# #     ordering = ("email",)
# #      # Specify unique related_name attributes for conflicting fields
# #     groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_groups')
# #     user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_user_permissions')


# # admin.site.register(CustomUser, CustomUserAdmin)
# # admin.site.register(Department)
# # admin.site.register(JobGroup)



# # @admin.register(Profile)
# # class ProfileAdmin(admin.ModelAdmin):
# #     list_display = ["photo", "date_joined"]