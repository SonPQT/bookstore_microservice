from rest_framework import serializers
from .models import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class AddCartItemSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(min_value=1)
    book_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)
