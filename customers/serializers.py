from rest_framework import serializers
from .models import Client  # Import the Client model

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'code', 'name', 'zone']  # Include relevant fields
