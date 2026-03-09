import os
from decimal import Decimal, InvalidOperation

import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Collection
from .serializers import CollectionSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
COMMENT_RATE_SERVICE_URL = os.getenv('COMMENT_RATE_SERVICE_URL', 'http://comment-rate-service:8000')


def _fetch_books():
    response = requests.get(f'{BOOK_SERVICE_URL}/books/', timeout=5)
    response.raise_for_status()
    return response.json()


def _fetch_book(book_id):
    response = requests.get(f'{BOOK_SERVICE_URL}/books/{book_id}/', timeout=5)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def _review_summary(book_id):
    try:
        response = requests.get(
            f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/summary/',
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {'review_count': 0, 'average_rating': None}


class CatalogBookList(APIView):
    def get(self, request):
        books = _fetch_books()
        keyword = (request.GET.get('keyword') or '').strip().lower()
        author = (request.GET.get('author') or '').strip().lower()
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        in_stock = (request.GET.get('in_stock') or '').strip().lower()
        sort_by = request.GET.get('sort')

        def price_ok(book):
            try:
                price = Decimal(str(book.get('price', '0')))
                if min_price not in (None, '') and price < Decimal(str(min_price)):
                    return False
                if max_price not in (None, '') and price > Decimal(str(max_price)):
                    return False
                return True
            except (InvalidOperation, ValueError):
                return False

        filtered = []
        for book in books:
            title_text = str(book.get('title', '')).lower()
            desc_text = str(book.get('description', '')).lower()
            author_text = str(book.get('author', '')).lower()
            if keyword and keyword not in title_text and keyword not in desc_text:
                continue
            if author and author not in author_text:
                continue
            if in_stock == 'true' and int(book.get('stock', 0)) < 1:
                continue
            if not price_ok(book):
                continue
            summary = _review_summary(book['id'])
            book['review_count'] = summary.get('review_count', 0)
            book['average_rating'] = summary.get('average_rating')
            filtered.append(book)

        if sort_by == 'price_asc':
            filtered.sort(key=lambda item: Decimal(str(item.get('price', '0'))))
        elif sort_by == 'price_desc':
            filtered.sort(key=lambda item: Decimal(str(item.get('price', '0'))), reverse=True)
        elif sort_by == 'rating_desc':
            filtered.sort(key=lambda item: (item.get('average_rating') or 0, item.get('review_count') or 0), reverse=True)
        else:
            filtered.sort(key=lambda item: int(item.get('id', 0)))

        return Response(filtered)


class CatalogBookDetail(APIView):
    def get(self, request, book_id):
        book = _fetch_book(book_id)
        if not book:
            return Response({'error': 'Book not found.'}, status=404)
        book['review_summary'] = _review_summary(book_id)
        try:
            review_response = requests.get(
                f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/',
                timeout=5,
            )
            if review_response.ok:
                book['reviews'] = review_response.json()
            else:
                book['reviews'] = []
        except requests.RequestException:
            book['reviews'] = []
        return Response(book)


class CollectionListCreate(generics.ListCreateAPIView):
    queryset = Collection.objects.all().order_by('id')
    serializer_class = CollectionSerializer


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'catalog-service', 'status': 'ok'})
