from django.urls import path
from .views import HealthView, OrderShipment, ShipmentCancel, ShipmentConfirm, ShipmentDetail, ShipmentList, ShipmentReserve

urlpatterns = [
    path('shipments/', ShipmentList.as_view()),
    path('shipments/<int:pk>/', ShipmentDetail.as_view()),
    path('shipments/reserve/', ShipmentReserve.as_view()),
    path('shipments/<int:pk>/confirm/', ShipmentConfirm.as_view()),
    path('shipments/<int:pk>/cancel/', ShipmentCancel.as_view()),
    path('shipments/order/<int:order_id>/', OrderShipment.as_view()),
    path('health/', HealthView.as_view()),
]
