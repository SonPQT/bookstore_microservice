import os
from decimal import Decimal

import requests
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://cart-service:8000')
PAY_SERVICE_URL = os.getenv('PAY_SERVICE_URL', 'http://pay-service:8000')
SHIP_SERVICE_URL = os.getenv('SHIP_SERVICE_URL', 'http://ship-service:8000')


def _fetch_cart(customer_id):
    response = requests.get(f'{CART_SERVICE_URL}/carts/{customer_id}/', timeout=5)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def _fetch_book(book_id):
    response = requests.get(f'{BOOK_SERVICE_URL}/books/{book_id}/', timeout=5)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def _reserve_book(book_id, quantity):
    response = requests.post(
        f'{BOOK_SERVICE_URL}/books/{book_id}/reserve/',
        json={'quantity': quantity},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def _release_book(book_id, quantity):
    try:
        requests.post(
            f'{BOOK_SERVICE_URL}/books/{book_id}/release/',
            json={'quantity': quantity},
            timeout=5,
        ).raise_for_status()
    except requests.RequestException:
        pass


def _reserve_payment(order_id, customer_id, amount, method):
    response = requests.post(
        f'{PAY_SERVICE_URL}/payments/reserve/',
        json={
            'order_id': order_id,
            'customer_id': customer_id,
            'amount': str(amount),
            'method': method,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def _confirm_payment(payment_id):
    response = requests.post(f'{PAY_SERVICE_URL}/payments/{payment_id}/confirm/', timeout=5)
    response.raise_for_status()
    return response.json()


def _cancel_payment(payment_id):
    try:
        requests.post(f'{PAY_SERVICE_URL}/payments/{payment_id}/cancel/', timeout=5).raise_for_status()
    except requests.RequestException:
        pass


def _reserve_shipment(order_id, customer_id, method, shipping_address):
    response = requests.post(
        f'{SHIP_SERVICE_URL}/shipments/reserve/',
        json={
            'order_id': order_id,
            'customer_id': customer_id,
            'method': method,
            'shipping_address': shipping_address or 'No address provided',
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def _confirm_shipment(shipment_id):
    response = requests.post(f'{SHIP_SERVICE_URL}/shipments/{shipment_id}/confirm/', timeout=5)
    response.raise_for_status()
    return response.json()


def _cancel_shipment(shipment_id):
    try:
        requests.post(f'{SHIP_SERVICE_URL}/shipments/{shipment_id}/cancel/', timeout=5).raise_for_status()
    except requests.RequestException:
        pass


class OrderListCreate(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('-id')
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            cart_payload = _fetch_cart(data['customer_id'])
        except requests.RequestException as exc:
            return Response(
                {'error': 'Unable to fetch cart.', 'details': str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not cart_payload or not cart_payload.get('items'):
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        prepared_items = []
        total_amount = Decimal('0.00')
        for item in cart_payload['items']:
            try:
                book = _fetch_book(item['book_id'])
            except requests.RequestException as exc:
                return Response(
                    {'error': 'Unable to fetch book.', 'details': str(exc)},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            if not book:
                return Response(
                    {'error': f"Book {item['book_id']} not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            quantity = int(item['quantity'])
            stock = int(book['stock'])
            if stock < quantity:
                return Response(
                    {'error': f"Book {book['title']} has insufficient stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            price = Decimal(str(book['price']))
            subtotal = price * quantity
            total_amount += subtotal
            prepared_items.append(
                {
                    'book_id': int(book['id']),
                    'title_snapshot': book['title'],
                    'price_snapshot': price,
                    'quantity': quantity,
                    'subtotal': subtotal,
                }
            )

        with transaction.atomic():
            order = Order.objects.create(
                customer_id=data['customer_id'],
                payment_method=data['payment_method'],
                shipping_method=data['shipping_method'],
                shipping_address=data.get('shipping_address', ''),
                total_amount=total_amount,
                status='PENDING',
            )
            for prepared in prepared_items:
                OrderItem.objects.create(order=order, **prepared)

        reserved_items = []
        payment = None
        shipment = None
        try:
            for prepared in prepared_items:
                _reserve_book(prepared['book_id'], prepared['quantity'])
                reserved_items.append((prepared['book_id'], prepared['quantity']))

            payment = _reserve_payment(
                order.id,
                data['customer_id'],
                total_amount,
                data['payment_method'],
            )
            shipment = _reserve_shipment(
                order.id,
                data['customer_id'],
                data['shipping_method'],
                data.get('shipping_address', ''),
            )
            payment = _confirm_payment(payment['id'])
            shipment = _confirm_shipment(shipment['id'])
        except requests.RequestException as exc:
            if shipment and shipment.get('id'):
                _cancel_shipment(shipment['id'])
            if payment and payment.get('id'):
                _cancel_payment(payment['id'])
            for book_id, quantity in reversed(reserved_items):
                _release_book(book_id, quantity)
            order.status = 'FAILED'
            order.save(update_fields=['status', 'updated_at'])
            payload = OrderSerializer(order).data
            payload['error'] = 'Order workflow failed.'
            payload['details'] = str(exc)
            return Response(payload, status=status.HTTP_502_BAD_GATEWAY)

        clear_warning = None
        try:
            requests.delete(f"{CART_SERVICE_URL}/carts/{data['customer_id']}/clear/", timeout=5).raise_for_status()
        except requests.RequestException as exc:
            clear_warning = str(exc)

        order.payment_id = payment['id']
        order.shipment_id = shipment['id']
        order.status = 'CONFIRMED'
        order.save(update_fields=['payment_id', 'shipment_id', 'status', 'updated_at'])

        payload = OrderSerializer(order).data
        payload['payment'] = payment
        payload['shipment'] = shipment
        if clear_warning:
            payload['warning'] = f'Order confirmed, but cart clear failed: {clear_warning}'
        return Response(payload, status=status.HTTP_201_CREATED)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomerOrders(APIView):
    def get(self, request, customer_id):
        orders = Order.objects.filter(customer_id=customer_id).order_by('-id')
        return Response(OrderSerializer(orders, many=True).data)


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'order-service', 'status': 'ok'})
