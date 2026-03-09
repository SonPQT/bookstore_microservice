import os
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')


class CartCreate(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, created = Cart.objects.get_or_create(customer_id=serializer.validated_data['customer_id'])
        return Response(
            {
                'message': 'Cart created.' if created else 'Cart already exists.',
                'cart': CartSerializer(cart).data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ViewCart(APIView):
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        items = CartItem.objects.filter(cart=cart).order_by('id')
        return Response(
            {
                'customer_id': customer_id,
                'cart_id': cart.id,
                'items': CartItemSerializer(items, many=True).data,
            }
        )


class AddCartItem(APIView):
    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cart, _ = Cart.objects.get_or_create(customer_id=data['customer_id'])
        try:
            book_response = requests.get(
                f"{BOOK_SERVICE_URL}/books/{data['book_id']}/",
                timeout=5,
            )
            if book_response.status_code == 404:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
            book_response.raise_for_status()
            book = book_response.json()
        except requests.RequestException as exc:
            return Response(
                {'error': 'Unable to validate book.', 'details': str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        existing_item = CartItem.objects.filter(cart=cart, book_id=data['book_id']).first()
        new_quantity = data['quantity']
        if existing_item:
            new_quantity += existing_item.quantity
        if int(book['stock']) < new_quantity:
            return Response(
                {'error': 'Requested quantity exceeds current stock.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if existing_item:
            existing_item.quantity = new_quantity
            existing_item.save(update_fields=['quantity'])
            item = existing_item
        else:
            item = CartItem.objects.create(
                cart=cart,
                book_id=data['book_id'],
                quantity=data['quantity'],
            )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetail(APIView):
    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
        quantity = request.data.get('quantity')
        if quantity is None or int(quantity) < 1:
            return Response({'error': 'Quantity must be >= 1.'}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = int(quantity)
        item.save(update_fields=['quantity'])
        return Response(CartItemSerializer(item).data)

    patch = put

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCart(APIView):
    def delete(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        deleted_count, _ = CartItem.objects.filter(cart=cart).delete()
        return Response({'message': 'Cart cleared.', 'deleted_items': deleted_count})


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'cart-service', 'status': 'ok'})
