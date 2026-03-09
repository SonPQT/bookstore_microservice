from django.urls import path
from .views import CustomerDetail, CustomerListCreate, HealthView

urlpatterns = [
    path('customers/', CustomerListCreate.as_view()),
    path('customers/<int:pk>/', CustomerDetail.as_view()),
    path('health/', HealthView.as_view()),
]
