from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

class ReserveShipmentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    customer_id = serializers.IntegerField(min_value=1)
    method = serializers.ChoiceField(choices=['STANDARD', 'EXPRESS'])
    shipping_address = serializers.CharField(max_length=255)
