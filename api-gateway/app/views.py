import os
import requests
from django.shortcuts import render

CUSTOMER_SERVICE_URL = os.getenv('CUSTOMER_SERVICE_URL', 'http://customer-service:8000')
BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://cart-service:8000')
STAFF_SERVICE_URL = os.getenv('STAFF_SERVICE_URL', 'http://staff-service:8000')
MANAGER_SERVICE_URL = os.getenv('MANAGER_SERVICE_URL', 'http://manager-service:8000')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:8000')
CATALOG_SERVICE_URL = os.getenv('CATALOG_SERVICE_URL', 'http://catalog-service:8000')
COMMENT_RATE_SERVICE_URL = os.getenv('COMMENT_RATE_SERVICE_URL', 'http://comment-rate-service:8000')
RECOMMENDER_SERVICE_URL = os.getenv('RECOMMENDER_SERVICE_URL', 'http://recommender-ai-service:8000')


def _safe_json(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=5, **kwargs)
        try:
            data = response.json()
        except Exception:
            data = {'raw': response.text}
        return response.status_code, data
    except requests.RequestException as exc:
        return 502, {'error': str(exc)}


def index(request):
    return render(request, 'index.html')


def books_page(request):
    message = None
    if request.method == 'POST':
        payload = {
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'description': request.POST.get('description', ''),
            'price': request.POST.get('price'),
            'stock': request.POST.get('stock'),
        }
        status_code, response_data = _safe_json('post', f'{STAFF_SERVICE_URL}/staff/books/', json=payload)
        message = {'status_code': status_code, 'data': response_data}
    _, books = _safe_json('get', f'{BOOK_SERVICE_URL}/books/')
    return render(request, 'books.html', {'books': books if isinstance(books, list) else [], 'message': message})


def catalog_page(request):
    params = {
        'keyword': request.GET.get('keyword', ''),
        'author': request.GET.get('author', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'in_stock': request.GET.get('in_stock', ''),
        'sort': request.GET.get('sort', ''),
    }
    _, books = _safe_json('get', f'{CATALOG_SERVICE_URL}/catalog/books/', params=params)
    return render(request, 'catalog.html', {'books': books if isinstance(books, list) else [], 'params': params})


def customers_page(request):
    message = None
    if request.method == 'POST':
        payload = {'name': request.POST.get('name'), 'email': request.POST.get('email')}
        status_code, response_data = _safe_json('post', f'{CUSTOMER_SERVICE_URL}/customers/', json=payload)
        message = {'status_code': status_code, 'data': response_data}
    _, customers = _safe_json('get', f'{CUSTOMER_SERVICE_URL}/customers/')
    return render(request, 'customers.html', {'customers': customers if isinstance(customers, list) else [], 'message': message})


def cart_page(request, customer_id):
    message = None
    if request.method == 'POST':
        payload = {
            'customer_id': customer_id,
            'book_id': request.POST.get('book_id'),
            'quantity': request.POST.get('quantity'),
        }
        status_code, response_data = _safe_json('post', f'{CART_SERVICE_URL}/cart-items/', json=payload)
        message = {'status_code': status_code, 'data': response_data}
    _, cart = _safe_json('get', f'{CART_SERVICE_URL}/carts/{customer_id}/')
    _, books = _safe_json('get', f'{BOOK_SERVICE_URL}/books/')
    return render(
        request,
        'cart.html',
        {
            'customer_id': customer_id,
            'cart': cart if isinstance(cart, dict) else {},
            'books': books if isinstance(books, list) else [],
            'message': message,
        },
    )


def orders_page(request, customer_id):
    message = None
    if request.method == 'POST':
        payload = {
            'customer_id': customer_id,
            'payment_method': request.POST.get('payment_method'),
            'shipping_method': request.POST.get('shipping_method'),
            'shipping_address': request.POST.get('shipping_address'),
        }
        status_code, response_data = _safe_json('post', f'{ORDER_SERVICE_URL}/orders/', json=payload)
        message = {'status_code': status_code, 'data': response_data}
    _, orders = _safe_json('get', f'{ORDER_SERVICE_URL}/orders/customer/{customer_id}/')
    _, cart = _safe_json('get', f'{CART_SERVICE_URL}/carts/{customer_id}/')
    return render(
        request,
        'orders.html',
        {
            'customer_id': customer_id,
            'orders': orders if isinstance(orders, list) else [],
            'cart': cart if isinstance(cart, dict) else {},
            'message': message,
        },
    )


def reviews_page(request, book_id):
    message = None
    if request.method == 'POST':
        payload = {
            'customer_id': request.POST.get('customer_id'),
            'book_id': book_id,
            'rating': request.POST.get('rating'),
            'comment': request.POST.get('comment', ''),
        }
        status_code, response_data = _safe_json('post', f'{COMMENT_RATE_SERVICE_URL}/reviews/', json=payload)
        message = {'status_code': status_code, 'data': response_data}
    _, book = _safe_json('get', f'{BOOK_SERVICE_URL}/books/{book_id}/')
    _, reviews = _safe_json('get', f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/')
    _, summary = _safe_json('get', f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/summary/')
    _, customers = _safe_json('get', f'{CUSTOMER_SERVICE_URL}/customers/')
    return render(
        request,
        'reviews.html',
        {
            'book': book if isinstance(book, dict) else {},
            'reviews': reviews if isinstance(reviews, list) else [],
            'summary': summary if isinstance(summary, dict) else {},
            'customers': customers if isinstance(customers, list) else [],
            'message': message,
        },
    )


def recommendations_page(request, customer_id):
    _, payload = _safe_json('get', f'{RECOMMENDER_SERVICE_URL}/recommendations/{customer_id}/')
    recommendations = []
    if isinstance(payload, dict):
        recommendations = payload.get('recommendations', [])
    return render(
        request,
        'recommendations.html',
        {'customer_id': customer_id, 'recommendations': recommendations},
    )


def dashboard_page(request):
    _, dashboard = _safe_json('get', f'{MANAGER_SERVICE_URL}/manager/dashboard/')
    _, health = _safe_json('get', f'{MANAGER_SERVICE_URL}/manager/health/')
    return render(request, 'dashboard.html', {'dashboard': dashboard, 'health': health})
