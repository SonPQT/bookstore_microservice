import os
import requests
from django.shortcuts import render, redirect

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


def _customer_context(request):
    """Inject customer_id and customer_name from session into template context."""
    return {
        'customer_id': request.session.get('customer_id'),
        'customer_name': request.session.get('customer_name'),
    }


def index(request):
    ctx = _customer_context(request)
    _, books = _safe_json('get', f'{CATALOG_SERVICE_URL}/catalog/books/', params={'sort': 'rating_desc'})
    ctx['featured_books'] = books[:8] if isinstance(books, list) else []
    return render(request, 'index.html', ctx)


def books_page(request):
    ctx = _customer_context(request)
    message = None
    if request.method == 'POST':
        action = request.POST.get('action', 'add')

        if action == 'edit':
            book_id = request.POST.get('book_id')
            payload = {
                'title': request.POST.get('title'),
                'author': request.POST.get('author'),
                'description': request.POST.get('description', ''),
                'genre': request.POST.get('genre', ''),
                'image_url': request.POST.get('image_url', ''),
                'price': request.POST.get('price'),
                'stock': request.POST.get('stock'),
            }
            status_code, response_data = _safe_json(
                'put', f'{STAFF_SERVICE_URL}/staff/books/{book_id}/', json=payload
            )
            if status_code == 200:
                message = {'status_code': 200, 'data': 'Cập nhật sách thành công!'}
            else:
                message = {'status_code': status_code, 'data': response_data}

        elif action == 'delete':
            book_id = request.POST.get('book_id')
            status_code, response_data = _safe_json(
                'delete', f'{STAFF_SERVICE_URL}/staff/books/{book_id}/'
            )
            if status_code == 204 or status_code == 200:
                message = {'status_code': 200, 'data': 'Đã xóa sách thành công!'}
            else:
                message = {'status_code': status_code, 'data': response_data}

        else:  # add
            payload = {
                'title': request.POST.get('title'),
                'author': request.POST.get('author'),
                'description': request.POST.get('description', ''),
                'genre': request.POST.get('genre', ''),
                'image_url': request.POST.get('image_url', ''),
                'price': request.POST.get('price'),
                'stock': request.POST.get('stock'),
            }
            status_code, response_data = _safe_json('post', f'{STAFF_SERVICE_URL}/staff/books/', json=payload)
            if status_code == 201:
                message = {'status_code': 201, 'data': 'Thêm sách thành công!'}
            else:
                message = {'status_code': status_code, 'data': response_data}

    _, books = _safe_json('get', f'{BOOK_SERVICE_URL}/books/')
    ctx.update({'books': books if isinstance(books, list) else [], 'message': message})
    return render(request, 'books.html', ctx)


def catalog_page(request):
    ctx = _customer_context(request)
    params = {
        'keyword': request.GET.get('keyword', ''),
        'author': request.GET.get('author', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'in_stock': request.GET.get('in_stock', ''),
        'sort': request.GET.get('sort', ''),
    }
    _, books = _safe_json('get', f'{CATALOG_SERVICE_URL}/catalog/books/', params=params)
    ctx.update({'books': books if isinstance(books, list) else [], 'params': params})
    return render(request, 'catalog.html', ctx)


def customers_page(request):
    """Handle login and register via POST (differentiated by 'action' hidden field)."""
    ctx = _customer_context(request)
    message = None

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'login':
            # ---- LOGIN via customer-service /customers/login/ ----
            payload = {
                'email': request.POST.get('email', '').strip(),
                'password': request.POST.get('password', ''),
            }
            status_code, response_data = _safe_json(
                'post', f'{CUSTOMER_SERVICE_URL}/customers/login/', json=payload
            )
            if status_code == 200 and isinstance(response_data, dict) and 'id' in response_data:
                request.session['customer_id'] = response_data['id']
                request.session['customer_name'] = response_data.get('name', 'Khách')
                return redirect('/')
            else:
                message = {'status_code': status_code, 'data': response_data}

        elif action == 'register':
            # ---- REGISTER via customer-service /customers/ ----
            payload = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
            }
            status_code, response_data = _safe_json(
                'post', f'{CUSTOMER_SERVICE_URL}/customers/', json=payload
            )
            message = {'status_code': status_code, 'data': response_data}

    ctx['message'] = message
    return render(request, 'customers.html', ctx)


def customer_logout(request):
    """Clear customer session and redirect to home."""
    request.session.flush()
    return redirect('/')


def cart_page(request, customer_id):
    ctx = _customer_context(request)
    message = None
    if request.method == 'POST':
        action = request.POST.get('action', 'add')

        if action == 'update_qty':
            item_id = request.POST.get('item_id')
            quantity = request.POST.get('quantity')
            status_code, response_data = _safe_json(
                'put', f'{CART_SERVICE_URL}/cart-items/{item_id}/',
                json={'quantity': int(quantity)}
            )
            message = {'status_code': status_code, 'data': response_data}

        elif action == 'delete_item':
            item_id = request.POST.get('item_id')
            status_code, response_data = _safe_json(
                'delete', f'{CART_SERVICE_URL}/cart-items/{item_id}/'
            )
            message = {'status_code': 200 if status_code == 204 else status_code,
                       'data': response_data if status_code != 204 else 'Đã xóa sản phẩm.'}

        elif action == 'clear_cart':
            status_code, response_data = _safe_json(
                'delete', f'{CART_SERVICE_URL}/carts/{customer_id}/clear/'
            )
            message = {'status_code': status_code, 'data': response_data}

        else:  # add
            payload = {
                'customer_id': customer_id,
                'book_id': request.POST.get('book_id'),
                'quantity': request.POST.get('quantity'),
            }
            status_code, response_data = _safe_json(
                'post', f'{CART_SERVICE_URL}/cart-items/', json=payload
            )
            message = {'status_code': status_code, 'data': response_data}

    _, cart = _safe_json('get', f'{CART_SERVICE_URL}/carts/{customer_id}/')
    _, books = _safe_json('get', f'{BOOK_SERVICE_URL}/books/')
    # Build book lookup for displaying names in cart
    book_map = {b['id']: b for b in books} if isinstance(books, list) else {}
    ctx.update({
        'customer_id': customer_id,
        'cart': cart if isinstance(cart, dict) else {},
        'books': books if isinstance(books, list) else [],
        'book_map': book_map,
        'message': message,
    })
    return render(request, 'cart.html', ctx)


def orders_page(request, customer_id):
    ctx = _customer_context(request)
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
    ctx.update({
        'customer_id': customer_id,
        'orders': orders if isinstance(orders, list) else [],
        'cart': cart if isinstance(cart, dict) else {},
        'message': message,
    })
    return render(request, 'orders.html', ctx)


def reviews_page(request, book_id):
    ctx = _customer_context(request)
    message = None
    if request.method == 'POST':
        action = request.POST.get('action', 'review')
        session_customer_id = request.session.get('customer_id')

        if action == 'add_to_cart' and session_customer_id:
            # Add book to cart with quantity 1
            payload = {
                'customer_id': session_customer_id,
                'book_id': book_id,
                'quantity': 1,
            }
            status_code, response_data = _safe_json(
                'post', f'{CART_SERVICE_URL}/cart-items/', json=payload
            )
            if status_code == 201:
                message = {'status_code': 201, 'data': 'Đã thêm sách vào giỏ hàng!'}
            else:
                message = {'status_code': status_code, 'data': response_data}

        elif session_customer_id:
            # Submit review
            payload = {
                'customer_id': session_customer_id,
                'book_id': book_id,
                'rating': request.POST.get('rating'),
                'comment': request.POST.get('comment', ''),
            }
            status_code, response_data = _safe_json(
                'post', f'{COMMENT_RATE_SERVICE_URL}/reviews/', json=payload
            )
            if status_code == 201 or status_code == 200:
                message = {'status_code': status_code, 'data': 'Đã gửi đánh giá thành công!'}
            else:
                message = {'status_code': status_code, 'data': response_data}
        else:
            message = {'status_code': 403, 'data': {'error': 'Bạn cần đăng nhập.'}}
    _, book = _safe_json('get', f'{BOOK_SERVICE_URL}/books/{book_id}/')
    _, reviews = _safe_json('get', f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/')
    _, summary = _safe_json('get', f'{COMMENT_RATE_SERVICE_URL}/reviews/book/{book_id}/summary/')
    ctx.update({
        'book': book if isinstance(book, dict) else {},
        'reviews': reviews if isinstance(reviews, list) else [],
        'summary': summary if isinstance(summary, dict) else {},
        'message': message,
    })
    return render(request, 'reviews.html', ctx)


def recommendations_page(request, customer_id):
    ctx = _customer_context(request)
    _, payload = _safe_json('get', f'{RECOMMENDER_SERVICE_URL}/recommendations/{customer_id}/')
    recommendations = []
    if isinstance(payload, dict):
        recommendations = payload.get('recommendations', [])
    ctx.update({'customer_id': customer_id, 'recommendations': recommendations})
    return render(request, 'recommendations.html', ctx)


def dashboard_page(request):
    ctx = _customer_context(request)
    _, dashboard = _safe_json('get', f'{MANAGER_SERVICE_URL}/manager/dashboard/')
    _, health = _safe_json('get', f'{MANAGER_SERVICE_URL}/manager/health/')
    ctx.update({'dashboard': dashboard, 'health': health})
    return render(request, 'dashboard.html', ctx)
