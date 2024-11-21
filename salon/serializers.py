from rest_framework import serializers
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

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class NailServiceCategorySerializer(serializers.ModelSerializer):
    
    nail_services = serializers.SerializerMethodField()
    
    class Meta:
        model = NailServiceCategory
        fields = '__all__'
        
    def get_nail_services(self, obj):
        nail_services = obj.nail_services.all()
        return NailServiceSerializer(nail_services, many=True).data


class NailServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NailService
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


class AppointmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentService
        fields = '__all__'
        depth = 2


class PayrollTurnSerializer(serializers.ModelSerializer):

    employee_payroll_turn_id = serializers.CharField(
        source='employee_payroll_turn.id', read_only=True)

    class Meta:
        model = PayrollTurn
        fields = '__all__'
        # depth = 1


class EmployeePayrollTurnSerializer(serializers.ModelSerializer):

    payroll_turns = PayrollTurnSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeePayrollTurn
        fields = ['id', 'employee', 'date', 'total_price', 'payroll_turns']


class EmployeePayrollSalarySerializer(serializers.Serializer):
    employee_id = serializers.CharField(required=False)
    employee__name = serializers.CharField(required=False)
    total_income = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    total_deduction = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    net_pay = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    gross_pay = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    pay_period_start = serializers.DateField(required=False)
    pay_period_end = serializers.DateField(required=False)
    employee__commission_rate = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False)
    total_tip = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    
    
class EmployeePayrollStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeePayrollTurn
        fields = ['date', 'total_price']
        # depth = 1


class EmployeePayslipsSerializer(serializers.ModelSerializer):

    gross_pay = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    net_pay = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = EmployeePayslips
        fields = '__all__'
        depth = 1
