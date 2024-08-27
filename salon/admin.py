from django.contrib import admin
from .models import Customer, Employee, NailService, Appointment, UserLevel, NailServiceCategory, Skill
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