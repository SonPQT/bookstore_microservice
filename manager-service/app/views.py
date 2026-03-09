import os
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Manager
from .serializers import ManagerSerializer

CUSTOMER_SERVICE_URL = os.getenv('CUSTOMER_SERVICE_URL', 'http://customer-service:8000')
BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://cart-service:8000')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:8000')
STAFF_SERVICE_URL = os.getenv('STAFF_SERVICE_URL', 'http://staff-service:8000')
CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL', 'http://catalog-service:8000')
PAY_SERVICE_URL = os.getenv('PAY_SERVICE_URL', 'http://pay-service:8000')
SHIP_SERVICE_URL = os.getenv('SHIP_SERVICE_URL', 'http://ship-service:8000')
COMMENT_RATE_SERVICE_URL = os.getenv('COMMENT_RATE_SERVICE_URL', 'http://comment-rate-service:8000')
RECOMMENDER_SERVICE_URL = os.getenv('RECOMMENDER_SERVICE_URL', 'http://recommender-ai-service:8000')


class ManagerListCreate(generics.ListCreateAPIView):
    queryset = Manager.objects.all().order_by('id')
    serializer_class = ManagerSerializer


class ManagerDetail(generics.RetrieveAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


def _safe_get_json(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


class DashboardView(APIView):
    def get(self, request):
        customers, customer_error = _safe_get_json(f'{CUSTOMER_SERVICE_URL}/customers/')
        books, book_error = _safe_get_json(f'{BOOK_SERVICE_URL}/books/')
        orders, order_error = _safe_get_json(f'{ORDER_SERVICE_URL}/orders/')
        staff, staff_error = _safe_get_json(f'{STAFF_SERVICE_URL}/staff/')
        collections, collection_error = _safe_get_json(f'{CATALOG_SERVICE_URL}/catalog/collections/')
        payments, payment_error = _safe_get_json(f'{PAY_SERVICE_URL}/payments/')
        shipments, shipment_error = _safe_get_json(f'{SHIP_SERVICE_URL}/shipments/')
        reviews, review_error = _safe_get_json(f'{COMMENT_RATE_SERVICE_URL}/reviews/')
        recommendation_logs, recommender_error = _safe_get_json(f'{RECOMMENDER_SERVICE_URL}/recommendations/logs/')
        return Response(
            {
                'customer_count': len(customers or []),
                'book_count': len(books or []),
                'order_count': len(orders or []),
                'staff_count': len(staff or []),
                'catalog_collection_count': len(collections or []),
                'payment_count': len(payments or []),
                'shipment_count': len(shipments or []),
                'review_count': len(reviews or []),
                'recommendation_request_count': len(recommendation_logs or []),
                'errors': {
                    'customers': customer_error,
                    'books': book_error,
                    'orders': order_error,
                    'staff': staff_error,
                    'catalog': collection_error,
                    'payments': payment_error,
                    'shipments': shipment_error,
                    'reviews': review_error,
                    'recommender': recommender_error,
                },
            }
        )


class SystemHealthView(APIView):
    def get(self, request):
        services = {
            'customer-service': f'{CUSTOMER_SERVICE_URL}/health/',
            'book-service': f'{BOOK_SERVICE_URL}/health/',
            'cart-service': f'{CART_SERVICE_URL}/health/',
            'staff-service': f'{STAFF_SERVICE_URL}/health/',
            'order-service': f'{ORDER_SERVICE_URL}/health/',
            'catalog-service': f'{CATALOG_SERVICE_URL}/health/',
            'pay-service': f'{PAY_SERVICE_URL}/health/',
            'ship-service': f'{SHIP_SERVICE_URL}/health/',
            'comment-rate-service': f'{COMMENT_RATE_SERVICE_URL}/health/',
            'recommender-ai-service': f'{RECOMMENDER_SERVICE_URL}/health/',
            'manager-service': 'local',
        }
        result = {}
        for name, url in services.items():
            if url == 'local':
                result[name] = {'status': 'ok'}
                continue
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                result[name] = response.json()
            except requests.RequestException as exc:
                result[name] = {'status': 'down', 'details': str(exc)}
        return Response(result)
