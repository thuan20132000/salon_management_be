from django.contrib import admin
from .models import Customer, Employee, Service, Appointment
# Register your models here.

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Appointment)

