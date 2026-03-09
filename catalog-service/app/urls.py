from django.urls import path
from .views import CatalogBookDetail, CatalogBookList, CollectionDetail, CollectionListCreate, HealthView

urlpatterns = [
    path('catalog/books/', CatalogBookList.as_view()),
    path('catalog/books/<int:book_id>/', CatalogBookDetail.as_view()),
    path('catalog/collections/', CollectionListCreate.as_view()),
    path('catalog/collections/<int:pk>/', CollectionDetail.as_view()),
    path('health/', HealthView.as_view()),
]
