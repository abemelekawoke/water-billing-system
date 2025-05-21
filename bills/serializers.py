from rest_framework import serializers
from .models import WaterBill

class WaterBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBill
        fields = ['id', 'code', 'month', 'year', 'previous_read', 'current_read', 'consumption', 'total_price', 'status', 'bank', 'payment_type']
        read_only_fields = ['id', 'code', 'month', 'year', 'previous_read', 'current_read', 'consumption', 'total_price']
    