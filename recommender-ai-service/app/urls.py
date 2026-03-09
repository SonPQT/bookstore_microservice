from django.urls import path
from .views import HealthView, RecommendationLogList, RecommendationView

urlpatterns = [
    path('recommendations/<int:customer_id>/', RecommendationView.as_view()),
    path('recommendations/logs/', RecommendationLogList.as_view()),
    path('health/', HealthView.as_view()),
]
