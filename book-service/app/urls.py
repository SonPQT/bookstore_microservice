from django.urls import path
from .views import BookDetail, BookListCreate, HealthView, ReleaseBook, ReserveBook

urlpatterns = [
    path('books/', BookListCreate.as_view()),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('books/<int:pk>/reserve/', ReserveBook.as_view()),
    path('books/<int:pk>/release/', ReleaseBook.as_view()),
    path('health/', HealthView.as_view()),
]
