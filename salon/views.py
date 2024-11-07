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

from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from salon.signals import update_employeee_daily_total_turn_price


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'employee': reverse('employee-list', request=request, format=format),
    })


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
    # Example of filtering by position
    # hire_date = django_filters.DateFilter(field_name='hire_date')  # Filter by exact hire date
    # is_active = django_filters.BooleanFilter(field_name='user__is_active')  # Filter based on user's active status
    employee = django_filters.CharFilter(
        field_name='employee')  # Filter by employee's id

    # filter by year and month
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    date = django_filters.CharFilter(field_name='date')

    class Meta:
        model = EmployeePayrollTurn
        fields = ['date', 'employee']  # List of fields to filter on


class EmployeePayrollTurnViewSet(viewsets.ModelViewSet):
    queryset = EmployeePayrollTurn.objects.all()
    serializer_class = EmployeePayrollTurnSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = EmployeePayrollTurnFilter

    # Custom action to retrieve employee's turns
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Prepare the custom response format
        response_data = {
            'total': len(queryset),  # Get the total number of turn
            'data': serializer.data,  # The serialized data
            # Get the total price of all turns
            'total_price': sum([float(turn['total_price']) for turn in serializer.data]),
        }

        return Response(response_data)
    
    @action(detail=False, methods=['get'], url_path='daily-turn')
    def get_daily_turn (self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # get first record
        queryset = queryset.first()
        serializer = self.get_serializer(queryset, many=False)
        print("Serializer: ", serializer.data)
        # Prepare the custom response format
        response_data = {
            'data': serializer.data,  # The serialized data
            # Get the total price of all turns
            # 'total_price': sum([float(turn['total_price']) for turn in serializer.data]),
        }

        return Response(serializer.data)

    @action(detail=True, methods=['get'],)
    def turns(self, request, pk=None):
        employee_turn = self.get_object()  # Get the employee instance
        # skills = employee.
        # turns =  employee_turn.employee_payroll_turn_set.all()
        employee_payroll_turns = PayrollTurn.objects.filter(
            employee_payroll_turn=employee_turn)
        employee_payroll_turns = PayrollTurnSerializer(
            employee_payroll_turns, many=True).data
        print("Turns: ", employee_payroll_turns)

        # payroll_turns_all = employee_turn.select_related('employee_payroll_turn__employee').all()
        # print("Turns: ", payroll_turns_all)
        return Response({'employee_turn': employee_payroll_turns})

        # Custom action to update a bulk of turns
    @action(detail=True, methods=['PUT'], url_path='bulk-update-turn', )
    def bulk_update_turns(self, request, pk=None):

        try:
            employee_payroll_turn = EmployeePayrollTurn.objects.get(pk=pk)
            print("Employee Payroll Turn: ", employee_payroll_turn)
            # return Response({'message': 'Bulk update or create successful!'}, status=status.HTTP_200_OK)

            turns = request.data
            for turn in turns:
                if 'id' in turn:
                    payroll_turn = PayrollTurn.objects.get(id=turn['id'])
                    if payroll_turn:
                        payroll_turn.price = turn['price']
                        payroll_turn.service_name = turn['service_name']
                        payroll_turn.save()
                else:
                    PayrollTurn.objects.create(
                        price=turn['price'],
                        service_name=turn['service_name'],
                        employee_payroll_turn=employee_payroll_turn
                    )

            update_employeee_daily_total_turn_price(employee_payroll_turn.id)

            return Response({'message': 'Bulk update or create successful!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Bulk update or create failed!'}, status=status.HTTP_400_BAD_REQUEST)


class PayrollTurnFilter(django_filters.FilterSet):
    # date = django_filters.CharFilter(field_name='date')  # Example of filtering by position
    # hire_date = django_filters.DateFilter(field_name='hire_date')  # Filter by exact hire date
    # is_active = django_filters.BooleanFilter(field_name='user__is_active')  # Filter based on user's active status
    employee_payroll_turn = django_filters.CharFilter(
        field_name='employee_payroll_turn')  # Filter by employee's id
    employee = django_filters.CharFilter(
        field_name='employee_payroll_turn__employee')  # Filter by employee's id
    date = django_filters.DateFilter(field_name='employee_payroll_turn__date')

    # # filter by year and month
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(
        field_name='employee_payroll_turn__date', lookup_expr='month')

    class Meta:
        model = PayrollTurn
        fields = ['employee_payroll_turn']  # List of fields to filter on


class PayrollTurnViewSet(viewsets.ModelViewSet):
    queryset = PayrollTurn.objects.all()
    serializer_class = PayrollTurnSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = PayrollTurnFilter

    # def list(self, _request, *_args, **_kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)

    #     # Prepare the custom response format
    #     response_data = {
    #         'total': len(queryset),  # Get the total number of turn
    #         'data': serializer.data,  # The serialized data
    #     }

    #     return Response(response_data)

    # Custom action to retrieve employee's turns
    @action(detail=False, methods=['get'])
    def turns(self, _request, _pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Prepare the custom response format
        response_data = {
            'total': len(queryset),  # Get the total number of turn
            # Get the total price of all turns
            'total_turn_price': sum([float(turn['price']) for turn in serializer.data]),
            'data': serializer.data,  # The serialized data
        }

        return Response(response_data)

    # Custom action to update a bulk of turns
    @action(detail=False, methods=['PUT'], url_path='bulk-update', )
    def bulk_update(self, request):

        try:

            turns = request.data
            employee_payroll_turn = EmployeePayrollTurn.objects.get(
                id=turns[0]['employee_payroll_turn'])
            for turn in turns:
                if 'id' in turn:
                    payroll_turn = PayrollTurn.objects.get(id=turn['id'])
                    if payroll_turn:
                        payroll_turn.price = turn['price']
                        payroll_turn.save()
                else:
                    PayrollTurn.objects.create(
                        price=turn['price'],
                        employee_payroll_turn=employee_payroll_turn
                    )

            update_employeee_daily_total_turn_price(employee_payroll_turn.id)

            return Response({'message': 'Bulk update or create successful!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Bulk update or create failed!'}, status=status.HTTP_400_BAD_REQUEST)
