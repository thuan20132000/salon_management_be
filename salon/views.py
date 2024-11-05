from rest_framework import viewsets
from .models import Employee, User, Skill, NailServiceCategory, NailService, Appointment, Customer, AppointmentService
from .serializers import (
    UserSerializer,
    SkillSerializer,
    EmployeeSerializer,
    NailServiceCategorySerializer,
    NailServiceSerializer,
    AppointmentSerializer,
    CustomerSerializer,
    AppointmentServiceSerializer
)
from rest_framework.response import Response
from rest_framework import status

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class NailServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = NailServiceCategory.objects.all()
    serializer_class = NailServiceCategorySerializer


class NailServiceViewSet(viewsets.ModelViewSet):
    queryset = NailService.objects.all()
    serializer_class = NailServiceSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AppointmentServiceViewSet(viewsets.ModelViewSet):
    queryset = AppointmentService.objects.all()
    serializer_class = AppointmentServiceSerializer
