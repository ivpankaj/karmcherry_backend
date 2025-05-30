from rest_framework import serializers
from .models import Employee
from users.models import User  # Update this if your user model has a different name


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # Assuming you have a UserSerializer defined in users/serializers.py


class EmployeeSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer()
    business = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'employee_type', 'business']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_employee=True)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
