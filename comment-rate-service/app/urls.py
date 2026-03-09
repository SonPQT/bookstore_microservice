from django.urls import path
from .views import BookReviewList, BookReviewSummary, CustomerReviewList, HealthView, ReviewDetail, ReviewListCreate

urlpatterns = [
    path('reviews/', ReviewListCreate.as_view()),
    path('reviews/<int:pk>/', ReviewDetail.as_view()),
    path('reviews/book/<int:book_id>/', BookReviewList.as_view()),
    path('reviews/book/<int:book_id>/summary/', BookReviewSummary.as_view()),
    path('reviews/customer/<int:customer_id>/', CustomerReviewList.as_view()),
    path('health/', HealthView.as_view()),
]
