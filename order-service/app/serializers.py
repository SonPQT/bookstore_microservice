from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(min_value=1)
    payment_method = serializers.ChoiceField(choices=['COD', 'MOMO', 'BANKING'])
    shipping_method = serializers.ChoiceField(choices=['STANDARD', 'EXPRESS'])
    shipping_address = serializers.CharField(max_length=255, required=False, allow_blank=True)
