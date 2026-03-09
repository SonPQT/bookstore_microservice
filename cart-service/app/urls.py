from django.urls import path
from .views import AddCartItem, CartCreate, CartItemDetail, ClearCart, HealthView, ViewCart

urlpatterns = [
    path('carts/', CartCreate.as_view()),
    path('carts/<int:customer_id>/', ViewCart.as_view()),
    path('carts/<int:customer_id>/clear/', ClearCart.as_view()),
    path('cart-items/', AddCartItem.as_view()),
    path('cart-items/<int:pk>/', CartItemDetail.as_view()),
    path('health/', HealthView.as_view()),
]
