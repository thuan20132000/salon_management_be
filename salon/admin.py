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
    EmployeePayslips,
    Salon,
    CustomerSalon,
    Payment,
    
)
# Register your models here.
from django.contrib import admin


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # fields = ('phone_number','commission_rate')
    exclude = ('user',)
    pass


@admin.register(NailService)
class NailServiceAdmin(admin.ModelAdmin):
    pass


class ApointmentServiceInline(admin.TabularInline):
    model = AppointmentService
    extra = 1
    
    # filter and display selection of services from appointment's salon_id

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    inlines = [ApointmentServiceInline]
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

class CustomerSalonInline(admin.TabularInline):
    model = CustomerSalon
    extra = 0

class EmployeeSalonInline(admin.TabularInline):
    model = Employee
    extra = 0
    fields = ('phone_number','commission_rate','name')

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    inlines = [CustomerSalonInline, EmployeeSalonInline]
    pass
    
@admin.register(CustomerSalon)
class CustomerSalonAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass