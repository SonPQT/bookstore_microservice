from django.urls import path
from .views import HealthView, OrderPayment, PaymentCancel, PaymentConfirm, PaymentDetail, PaymentList, PaymentReserve

urlpatterns = [
    path('payments/', PaymentList.as_view()),
    path('payments/<int:pk>/', PaymentDetail.as_view()),
    path('payments/reserve/', PaymentReserve.as_view()),
    path('payments/<int:pk>/confirm/', PaymentConfirm.as_view()),
    path('payments/<int:pk>/cancel/', PaymentCancel.as_view()),
    path('payments/order/<int:order_id>/', OrderPayment.as_view()),
    path('health/', HealthView.as_view()),
]
