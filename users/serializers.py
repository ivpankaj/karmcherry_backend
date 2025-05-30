# users/serializers.py

from rest_framework import serializers
from .models import User
from django.db import transaction
from .task import send_verification_email_task

from django.db import transaction
from .task import send_verification_email_task

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "is_business_owner")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save()

            host = request.META.get('HTTP_HOST', 'localhost:8000')

            # Ensures task is called only after DB commit
            transaction.on_commit(lambda: send_verification_email_task.delay(
                user_id=user.id,
                request_data={'host': host}
            ))

            return user

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_active:
                raise serializers.ValidationError("Email is already verified.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")

    def send_verification_email(self, email, request):
        from .utils import send_verification_email
        user = User.objects.get(email=email)
        return send_verification_email(user, request)
