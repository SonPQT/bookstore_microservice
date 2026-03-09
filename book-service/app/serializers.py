from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class StockAdjustSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
