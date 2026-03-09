from django.urls import path
from .views import HealthView, StaffBookProxy, StaffBookProxyDetail, StaffDetail, StaffListCreate

urlpatterns = [
    path('staff/', StaffListCreate.as_view()),
    path('staff/<int:pk>/', StaffDetail.as_view()),
    path('staff/books/', StaffBookProxy.as_view()),
    path('staff/books/<int:book_id>/', StaffBookProxyDetail.as_view()),
    path('health/', HealthView.as_view()),
]
