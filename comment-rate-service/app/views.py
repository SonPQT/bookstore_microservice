import os
import requests
from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Review
from .serializers import ReviewSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
CUSTOMER_SERVICE_URL = os.getenv('CUSTOMER_SERVICE_URL', 'http://customer-service:8000')


def _exists(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-updated_at')
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not _exists(f"{CUSTOMER_SERVICE_URL}/customers/{data['customer_id']}/"):
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not _exists(f"{BOOK_SERVICE_URL}/books/{data['book_id']}/"):
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        review, created = Review.objects.update_or_create(
            customer_id=data['customer_id'],
            book_id=data['book_id'],
            defaults={'rating': data['rating'], 'comment': data.get('comment', '')},
        )
        response_serializer = ReviewSerializer(review)
        return Response(
            {
                'message': 'Review created.' if created else 'Review updated.',
                'review': response_serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class BookReviewList(APIView):
    def get(self, request, book_id):
        reviews = Review.objects.filter(book_id=book_id).order_by('-updated_at')
        return Response(ReviewSerializer(reviews, many=True).data)


class CustomerReviewList(APIView):
    def get(self, request, customer_id):
        reviews = Review.objects.filter(customer_id=customer_id).order_by('-updated_at')
        return Response(ReviewSerializer(reviews, many=True).data)


class BookReviewSummary(APIView):
    def get(self, request, book_id):
        summary = Review.objects.filter(book_id=book_id).aggregate(
            review_count=Count('id'),
            average_rating=Avg('rating'),
        )
        avg = summary['average_rating']
        return Response(
            {
                'book_id': book_id,
                'review_count': summary['review_count'] or 0,
                'average_rating': round(float(avg), 2) if avg is not None else None,
            }
        )


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'comment-rate-service', 'status': 'ok'})
