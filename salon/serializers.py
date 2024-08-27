from rest_framework import serializers
from .models import Employee, User, Skill, NailServiceCategory, NailService, Appointment

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
    class Meta:
        model = NailServiceCategory
        fields = '__all__'

class NailServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NailService
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'