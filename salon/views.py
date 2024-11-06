from rest_framework import viewsets
from .models import (
    Employee,
    User,
    Skill,
    NailServiceCategory,
    NailService,
    Appointment,
    Customer,
    AppointmentService,
    EmployeePayrollTurn,
    PayrollTurn
)
from .serializers import (
    UserSerializer,
    SkillSerializer,
    EmployeeSerializer,
    NailServiceCategorySerializer,
    NailServiceSerializer,
    AppointmentSerializer,
    CustomerSerializer,
    AppointmentServiceSerializer,
    EmployeePayrollTurnSerializer,
    PayrollTurnSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters import rest_framework as django_filters


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

class EmployeePayrollTurnFilter(django_filters.FilterSet):
    date = django_filters.CharFilter(field_name='date')  # Example of filtering by position
    # hire_date = django_filters.DateFilter(field_name='hire_date')  # Filter by exact hire date
    # is_active = django_filters.BooleanFilter(field_name='user__is_active')  # Filter based on user's active status
    employee = django_filters.CharFilter(field_name='employee')  # Filter by employee's id
    class Meta:
        model = EmployeePayrollTurn
        fields = ['date','employee']  # List of fields to filter on


class EmployeePayrollTurnViewSet(viewsets.ModelViewSet):
    queryset = EmployeePayrollTurn.objects.all()
    serializer_class = EmployeePayrollTurnSerializer
    
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = EmployeePayrollTurnFilter


    # Custom action to retrieve employee's turns
    @action(detail=True, methods=['get'])
    def turns(self, request, pk=None):
        employee_turn = self.get_object()  # Get the employee instance
        # skills = employee.
        # turns =  employee_turn.employee_payroll_turn_set.all()
        employee_payroll_turns = PayrollTurn.objects.filter(employee_payroll_turn=employee_turn)
        employee_payroll_turns = PayrollTurnSerializer(employee_payroll_turns, many=True).data
        print("Turns: ", employee_payroll_turns)
        
        # payroll_turns_all = employee_turn.select_related('employee_payroll_turn__employee').all()
        # print("Turns: ", payroll_turns_all)
        return Response({'employee_turn': employee_payroll_turns})


class PayrollTurnViewSet(viewsets.ModelViewSet):
    queryset = PayrollTurn.objects.all()
    serializer_class = PayrollTurnSerializer
