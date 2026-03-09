from django.urls import path
from .views import DashboardView, ManagerDetail, ManagerListCreate, SystemHealthView

urlpatterns = [
    path('managers/', ManagerListCreate.as_view()),
    path('managers/<int:pk>/', ManagerDetail.as_view()),
    path('manager/dashboard/', DashboardView.as_view()),
    path('manager/health/', SystemHealthView.as_view()),
]
