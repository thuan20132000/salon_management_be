from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
    PayrollTurn,
    EmployeePayslips,
    Salon
)
from django.db import models
from django.db.models import F, Sum, DecimalField, FloatField
from decimal import Decimal
from django.db.models.functions import Round, Greatest

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
    PayrollTurnSerializer,
    EmployeePayrollStatisticSerializer,
    EmployeePayslipsSerializer,
    EmployeePayrollSalarySerializer,
    SalonSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters import rest_framework as django_filters

from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from salon.signals import update_employeee_daily_total_turn_price
from salon.enums import EmployeeShareEnum
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework import permissions

import time

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'employee': reverse('employee-list', request=request, format=format),
    })


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.user
        response = super().post(request, *args, **kwargs)

        response.data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return response


class EmployeeFilter(django_filters.FilterSet):
    # Example of filtering by position
    # hire_date = django_filters.DateFilter(field_name='hire_date')  # Filter by exact hire date
    # is_active = django_filters.BooleanFilter(field_name='user__is_active')  # Filter based on user's active status
    name = django_filters.CharFilter(
        field_name='name')  # Filter by employee's name
    phone_number = django_filters.CharFilter(
        field_name='phone_number')  # Filter by employee's phone number
    email = django_filters.CharFilter(
        field_name='email')  # Filter by employee's email
    position = django_filters.CharFilter(
        field_name='position')  # Filter by employee's position
    user = django_filters.CharFilter(
        field_name='user')  # Filter by employee's id
    salon = django_filters.CharFilter(
        field_name='salon')  # Filter by salon's id

    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'email',
                  'position', 'user']  # List of fields to filter on


class EmployeeViewSet(viewsets.ModelViewSet):

    # permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = EmployeeFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SkillViewSet(viewsets.ModelViewSet):

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class NailServiceCategoryFilter(django_filters.FilterSet):
    salon = django_filters.CharFilter(
        field_name='salon')  # Filter by salon's id


class NailServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = NailServiceCategory.objects.all()
    serializer_class = NailServiceCategorySerializer
    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = NailServiceCategoryFilter


class NailServiceFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category')  # Filter by category's id
    salon = django_filters.CharFilter(
        field_name='salon')  # Filter by salon's id


class NailServiceViewSet(viewsets.ModelViewSet):
    queryset = NailService.objects.all()
    serializer_class = NailServiceSerializer
    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = NailServiceFilter


class AppointmentFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(
        field_name='customer')  # Filter by customer's id
    employee = django_filters.CharFilter(
        field_name='employee')  # Filter by employee's id
    date = django_filters.DateFilter(field_name='date')  # Filter by date
    salon = django_filters.CharFilter(
        field_name='salon')  # Filter by salon's id


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = AppointmentFilter


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name')  # Filter by customer's name
    phone_number = django_filters.CharFilter(
        field_name='phone_number')  # Filter by customer's phone number
    email = django_filters.CharFilter(
        field_name='email')  # Filter by customer's email
    user = django_filters.CharFilter(
        field_name='user')  # Filter by customer's id

    # filter customer by salon_id
    salon = django_filters.CharFilter(
        field_name='customersalon__salon_id')  # Filter by salon's id


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = CustomerFilter


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
    date_range = django_filters.DateFromToRangeFilter(field_name='date')
    # start_date = django_filters.DateFromToRangeFilter( field_name='date')
    # end_date = django_filters.DateFromToRangeFilter(
    #     field_name='date', lookup_expr='lte')

    class Meta:
        model = EmployeePayrollTurn
        fields = ['date', 'employee']  # List of fields to filter on


class EmployeePayrollTurnViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    queryset = EmployeePayrollTurn.objects.all()
    serializer_class = EmployeePayrollTurnSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = EmployeePayrollTurnFilter

    # Custom action to retrieve employee's turns
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        total_price = queryset.aggregate(
            total_price=models.Sum('total_price'))['total_price'] or 0

        # Prepare the custom response format
        response_data = {
            'total': len(queryset),  # Get the total number of turn
            'data': serializer.data,  # The serialized data
            # Get the total price of all turns
            'total_price': total_price,
        }

        return Response(response_data)

    # Custom action to get employee's statistic by date range
    @action(detail=False, methods=['get'], url_path='statistics')
    def get_statistic(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # sum all total_price
        sum_total_price = queryset.aggregate(
            total_price=models.Sum('total_price'))['total_price'] or 0

        serializer = EmployeePayrollStatisticSerializer(queryset, many=True)

        # Prepare the custom response format
        response_data = {
            'data': serializer.data,  # The serialized data
            'date_range_after': request.query_params.get('date_range_after'),
            'date_range_before': request.query_params.get('date_range_before'),
            'total_price': sum_total_price
        }

        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='daily-turn')
    def get_daily_turn(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # get first record
        queryset = queryset.first()
        serializer = self.get_serializer(queryset, many=False)
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

    # show employee income by date range

    @action(detail=False, methods=['GET'], url_path='income')
    def show_income(self, request, pk=None):
        try:
            auth = request.user
            print("USER AUTH: ", auth)

            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            employee_ids = request.query_params.get('employee_ids')
            employee_ids = employee_ids.split(",")

            queryset = EmployeePayrollTurn.objects.filter(
                employee_id__in=employee_ids, date__range=[start_date, end_date]).values(
                'employee_id',
                'employee__commission_rate',
                'employee__name',
            )

            queryset = queryset.annotate(
                gross_pay=Round(
                    Sum(F('total_price'), output_field=FloatField()), precision=2),
                net_pay=Round(Sum(F('total_price'), output_field=FloatField(
                )) * F('employee__commission_rate'), precision=2, output_field=FloatField()),
            )

            queryset = list(queryset)
            serilizers = EmployeePayrollSalarySerializer(
                data=queryset, many=True)
            if serilizers.is_valid():
                return Response(serilizers.data, status=status.HTTP_200_OK)
            else:
                return Response(serilizers.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Error: ", e)
            return Response({'message': 'Income calculation failed!'}, status=status.HTTP_400_BAD_REQUEST)


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

    permission_classes = [permissions.IsAuthenticated]

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


class EmployeePayslipsFilter(django_filters.FilterSet):

    gross_salary = django_filters.NumberFilter(field_name='gross_salary')
    net_salary = django_filters.NumberFilter(field_name='net_salary')
    pay_period_start = django_filters.DateFilter(field_name='pay_period_start')
    pay_period_end = django_filters.DateFilter(field_name='pay_period_end')
    employee = django_filters.CharFilter(
        field_name='employee')  # Filter by employee's id

    class Meta:
        model = EmployeePayslips
        fields = ['gross_salary', 'net_salary',
                  'pay_period_start', 'pay_period_end']


class EmployeePayslipsViewSet(viewsets.ModelViewSet):
    queryset = EmployeePayslips.objects.all()
    serializer_class = EmployeePayslipsSerializer

    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = EmployeePayslipsFilter

    # Custom action to create a payslip for employee
    # @action(detail=True, methods=['POST'],)
    # def create_payslip(self, request):
    #     try:
    #         print("pk:: ")
    #         employee = Employee.objects.get(pk=1)

    #         start_date = request.data['pay_period_start']
    #         end_date = request.data['pay_period_end']

    #         # Get all employee's payroll turns within the pay period
    #         queryset = EmployeePayrollTurn.objects.filter(
    #             employee=employee, date__range=[start_date, end_date])

    #         sum_total_price = queryset.aggregate(
    #             total_price=models.Sum('total_price'))['total_price'] or 0

    #         # payslip = EmployeePayslips.objects.create(
    #         #     employee=employee,
    #         #     pay_period_start=request.data['pay_period_start'],
    #         #     pay_period_end=request.data['pay_period_end'],
    #         #     gross_salary=request.data['gross_salary'],
    #         #     net_salary=request.data['net_salary']
    #         # )

    #         res = {
    #             sum_total_price: sum_total_price
    #         }

    #         return Response(res, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'message': 'Payslip creation failed!'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:

            start_date = request.data.get('pay_period_start')
            end_date = request.data.get('pay_period_end')
            employee_id = request.data.get('employee')
            bonus = request.data.get('bonus')
            share = request.data.get('share') or None

            if share is None:
                share = EmployeeShareEnum.COMMON_SHARE.value

            employee = Employee.objects.get(pk=employee_id)
            # Get all employee's payroll turns within the pay period
            queryset = EmployeePayrollTurn.objects.filter(
                employee=employee, date__range=[start_date, end_date])

            gross_salary = queryset.aggregate(
                total_price=models.Sum('total_price'))['total_price'] or 0
            # bonus = float(bonus) if bonus else float(0)
            net_salary = float(gross_salary) * \
                float(share)  # 60% of gross salary
            if bonus and float(bonus) > 0:
                net_salary = net_salary + float(bonus)

            payslip = EmployeePayslips.objects.create(
                employee=employee,
                pay_period_start=request.data['pay_period_start'],
                pay_period_end=request.data['pay_period_end'],
                gross_salary=gross_salary,
                net_salary=net_salary,
                share=share,
                bonus=bonus
            )

            payroll_serilizers = EmployeePayrollTurnSerializer(
                queryset, many=True).data
            payslips_serializers = EmployeePayslipsSerializer(payslip).data

            res_data = {
                "payslip": payslips_serializers,
                "payroll_turns": payroll_serilizers
            }
            return Response(res_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Payslip creation failed!'}, status=status.HTTP_400_BAD_REQUEST)
        # return super().create(request, *args, **kwargs)


class SalonViewSet(viewsets.ModelViewSet):

    # permission_classes = [permissions.IsAuthenticated]
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

    @action(detail=True, methods=['get'], url_path='employees')
    def get_employees_by_salon(self, request, pk=None):
        salon = self.get_object()  # Get the salon instance
        employees = salon.employee_set.all()
        employees = EmployeeSerializer(employees, many=True).data
        return Response({'employees': employees})

    @action(detail=True, methods=['get'], url_path='nail-services')
    def get_nail_services(self, request, pk=None):
        salon = self.get_object()  # Get the salon instance
        nail_services = salon.nailservice_set.all()
        nail_services = NailServiceSerializer(nail_services, many=True).data
        return Response({'nail_services': nail_services})

    @action(detail=True, methods=['post'], url_path='nail-service')
    def create_nail_service(self, request, pk=None):
        data = request.data.copy()
        data['salon'] = pk
        serializer = NailServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='nail-service/(?P<service_id>\d+)/update')
    def update_nail_service(self, request, pk=None, service_id=None):
        data = request.data.copy()

        instance = NailService.objects.get(pk=service_id)

        serializer = NailServiceSerializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='nail-service/(?P<service_id>\d+)/delete')
    def delete_nail_service(self, request, pk=None, service_id=None):
        try:
            # comment: 
            instance = NailService.objects.get(pk=service_id)
            instance.delete()
            return Response({'message': 'Service deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
        # end try
    
    @action(detail=True, methods=['get'], url_path='nail-service-categories')
    def get_nail_service_categories(self, request, pk=None):
        print("Get Nail Service Categories")
        salon = self.get_object()
        nail_service_categories = salon.nailservicecategory_set.all()
        nail_service_categories = NailServiceCategorySerializer(
            nail_service_categories, many=True).data
        return Response(nail_service_categories)

    @action(detail=True, methods=['post'], url_path='nail-service-category')
    def create_nail_service_category(self, request, pk=None):
        data = request.data.copy()
        data['salon'] = pk
        serializer = NailServiceCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='nail-service-category/(?P<category_id>\d+)/update')
    def update_nail_service_category(self, request, pk=None, category_id=None):
        data = request.data.copy()

        instance = NailServiceCategory.objects.get(pk=category_id)

        serializer = NailServiceCategorySerializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='nail-service-category/(?P<category_id>\d+)/delete')
    def delete_nail_service_category(self, request, pk=None, category_id=None):
        try:
            # comment: 
            instance = NailServiceCategory.objects.get(pk=category_id)
            instance.delete()
            return Response({'message': 'Category deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
        # end try

    @action(detail=True, methods=['get'], url_path='appointments')
    def get_appointments(self, request, pk=None):
        salon = self.get_object()  # Get the salon instance
        appointments = salon.appointment_set.all()
        appointments = AppointmentSerializer(appointments, many=True).data
        return Response({'appointments': appointments})

    @action(detail=True, methods=['get'], url_path='customers')
    def get_customers(self, request, pk=None):
        salon = self.get_object()  # Get the salon instance
        customers = salon.customers.all()
        customers = CustomerSerializer(customers, many=True).data
        return Response({'customers': customers})

    @action(detail=True, methods=['get'], url_path='employees')
    def get_employees(self, request, pk=None):
        salon = self.get_object()  # Get the salon instance
        employees = salon.employees.all()
        employees_serializer = EmployeeSerializer(employees, many=True).data
        return Response(employees_serializer)
    
    @action(detail=True, methods=['post'], url_path='employee')
    def create_employee(self, request, pk=None):
        data = request.data.copy()
        data['salon'] = pk
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='employee/(?P<employee_id>\d+)/update')
    def update_employee(self, request, pk=None, employee_id=None):
        data = request.data.copy()

        instance = Employee.objects.get(pk=employee_id)

        serializer = EmployeeSerializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='employee/(?P<employee_id>\d+)/delete')
    def delete_employee(self, request, pk=None, employee_id=None):
        try:
            # comment: 
            instance = Employee.objects.get(pk=employee_id)
            instance.delete()
            return Response({'message': 'Employee deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
        # end try
        
    @action(detail=True, methods=['get'], url_path='employee/(?P<employee_id>\d+)')
    def get_employee(self, request, pk=None, employee_id=None):
        salon = self.get_object()  # Get the salon instance
        employee = salon.employees.get(pk=employee_id)
        employee_serializer = EmployeeSerializer(employee).data
        return Response(employee_serializer)