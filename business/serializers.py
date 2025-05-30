from rest_framework import serializers
from .models import Business

class BusinessSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Business
        fields = '__all__'
