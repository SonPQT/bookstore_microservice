import os

import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RecommendationRequest
from .serializers import RecommendationRequestSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
COMMENT_RATE_SERVICE_URL = os.getenv('COMMENT_RATE_SERVICE_URL', 'http://comment-rate-service:8000')


def _get_json(url, default):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return default


class RecommendationView(APIView):
    def get(self, request, customer_id):
        limit = int(request.GET.get('limit', 5))
        books = _get_json(f'{BOOK_SERVICE_URL}/books/', [])
        customer_reviews = _get_json(f'{COMMENT_RATE_SERVICE_URL}/reviews/customer/{customer_id}/', [])
        reviewed_book_ids = {item['book_id'] for item in customer_reviews if 'book_id' in item}

        scored_books = []
        for book in books:
            if int(book.get('stock', 0)) < 1:
                continue
            if int(book['id']) in reviewed_book_ids:
                continue
            summary = _get_json(
                f"{COMMENT_RATE_SERVICE_URL}/reviews/book/{book['id']}/summary/",
                {'review_count': 0, 'average_rating': None},
            )
            score = (
                float(summary['average_rating']) if summary.get('average_rating') is not None else 0.0,
                int(summary.get('review_count', 0)),
                int(book.get('stock', 0)),
            )
            enriched = dict(book)
            enriched['review_count'] = summary.get('review_count', 0)
            enriched['average_rating'] = summary.get('average_rating')
            enriched['score'] = score
            scored_books.append(enriched)

        scored_books.sort(key=lambda item: item['score'], reverse=True)
        recommendations = scored_books[: max(limit, 1)]
        RecommendationRequest.objects.create(
            customer_id=customer_id,
            strategy='top-rated',
            result_count=len(recommendations),
        )
        for item in recommendations:
            item.pop('score', None)
        return Response({'customer_id': customer_id, 'recommendations': recommendations})


class RecommendationLogList(generics.ListAPIView):
    queryset = RecommendationRequest.objects.all().order_by('-id')
    serializer_class = RecommendationRequestSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'recommender-ai-service', 'status': 'ok'})
