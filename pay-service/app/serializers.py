from decimal import Decimal
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ReservePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    customer_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    method = serializers.ChoiceField(choices=['COD', 'MOMO', 'BANKING'])
