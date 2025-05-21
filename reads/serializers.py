from rest_framework import serializers
from .models import WaterRead

class WaterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterRead
        fields = ['id', 'code', 'month', 'year', 'current_read']
        read_only_fields = ['id', 'code', 'month', 'year']
