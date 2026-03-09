from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('books/', views.books_page, name='books_page'),
    path('catalog/', views.catalog_page, name='catalog_page'),
    path('customers/', views.customers_page, name='customers_page'),
    path('cart/<int:customer_id>/', views.cart_page, name='cart_page'),
    path('orders/<int:customer_id>/', views.orders_page, name='orders_page'),
    path('reviews/<int:book_id>/', views.reviews_page, name='reviews_page'),
    path('recommendations/<int:customer_id>/', views.recommendations_page, name='recommendations_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
]
