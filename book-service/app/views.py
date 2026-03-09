from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer, StockAdjustSerializer


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveBook(APIView):
    def post(self, request, pk):
        serializer = StockAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=pk)
                if book.stock < quantity:
                    return Response(
                        {'error': 'Not enough stock available.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                book.stock -= quantity
                book.save(update_fields=['stock', 'updated_at'])
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Stock reserved.', 'book': BookSerializer(book).data})


class ReleaseBook(APIView):
    def post(self, request, pk):
        serializer = StockAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=pk)
                book.stock += quantity
                book.save(update_fields=['stock', 'updated_at'])
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Stock released.', 'book': BookSerializer(book).data})


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'book-service', 'status': 'ok'})
