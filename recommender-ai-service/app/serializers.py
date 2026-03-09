from rest_framework import serializers
from .models import RecommendationRequest

class RecommendationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationRequest
        fields = '__all__'
