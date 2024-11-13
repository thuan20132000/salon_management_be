from django.contrib import admin
from .models import (
    Customer,
    Employee,
    NailService,
    Appointment,
    UserLevel,
    NailServiceCategory,
    Skill,
    AppointmentService,
    EmployeePayrollTurn,
    PayrollTurn,
    EmployeePayslips
)
# Register your models here.
from django.contrib import admin


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(NailService)
class NailServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(NailServiceCategory)
class NailServiceCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(AppointmentService)
class AppointmentServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeePayrollTurn)
class EmployeePayrollTurnAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'total_price')  # Display these fields in the list view
    pass
    # list_display = ('user', 'phone_number')  # Display these fields in the list view
    # search_fields = ('user__username', 'user__email', 'position')  # Search by username, email, or position
    # list_filter = ('position',)  # Add filter options for the list view


@admin.register(PayrollTurn)
class PayrollTurnAdmin(admin.ModelAdmin):
    pass

@admin.register(EmployeePayslips)
class EmployeePayslipsAdmin(admin.ModelAdmin):
    pass
