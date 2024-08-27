# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string


class User(AbstractUser):
    # Add any additional fields for the User model if needed
    groups = models.ManyToManyField(
        Group,
        related_name='salon_user_set',  # Custom related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='salon_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        # Custom related_name to avoid conflict
        related_name='salon_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='salon_user_permissions',
    )

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserLevel(models.Model):
    LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Intermediate', 'Intermediate'),
        ('Senior', 'Senior'),
        ('Manager', 'Manager'),
        ('Owner', 'Owner'),
    ]

    name = models.CharField(
        max_length=255, choices=LEVEL_CHOICES, default='Junior')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(User):

    EMPLOYEE_STATUS = [
        ('1', 'Active'),
        ('2', 'Inactive'),
        ('3', 'On Leave'),
        ('4', 'Resigned'),
    ]

    phone_number = models.CharField(max_length=15)
    level = models.ForeignKey(
        UserLevel, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=EMPLOYEE_STATUS, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(Skill, related_name='employees')

    def __str__(self):
        return f"{self.username} - {self.job_title}"

    def save(self, *args, **kwargs):
        print('password:: ', self.password)
        if not self.password:
            self.set_password(get_random_string())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Customer(User):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class NailServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_online_booking = models.BooleanField(default=False)
    is_check_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NailService(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(
        help_text="Duration of the service (e.g., 1 hour)")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='nail_services/', blank=True, null=True)
    category = models.ForeignKey(
        NailServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):

    APPOINTMENT_STATUS = [
        ('1', 'Pending'),
        ('2', 'Confirmed'),
        ('3', 'Cancelled'),
        ('4', 'Completed'),
    ]

    datetime = models.DateTimeField()
    duration = models.IntegerField(
        help_text="Duration of the appointment (e.g., 1 hour)", blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=APPOINTMENT_STATUS, default='Pending')
    services = models.ManyToManyField(NailService)
    type = models.CharField(max_length=50, blank=True, null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.customer} on {self.datetime}"


