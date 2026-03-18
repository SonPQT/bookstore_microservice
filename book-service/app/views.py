from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookSerializer, StockAdjustSerializer


@extend_schema(tags=['Books'])
class BookListCreate(generics.ListCreateAPIView):
    """
    list:
    Trả về danh sách tất cả sách trong hệ thống.

    create:
    Tạo một cuốn sách mới.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer


@extend_schema(tags=['Books'])
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve:
    Trả về thông tin chi tiết của một cuốn sách theo ID.

    update:
    Cập nhật toàn bộ thông tin cuốn sách.

    partial_update:
    Cập nhật một phần thông tin cuốn sách.

    destroy:
    Xóa cuốn sách khỏi hệ thống.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveBook(APIView):
    @extend_schema(
        tags=['Stock Management'],
        summary='Đặt trước tồn kho sách',
        description=(
            'Giảm số lượng tồn kho của sách đi một lượng nhất định khi có đơn hàng. '
            'Sử dụng database-level locking để đảm bảo tính nhất quán trong môi trường concurrent.'
        ),
        request=StockAdjustSerializer,
        responses={
            200: OpenApiResponse(
                response=BookSerializer,
                description='Đặt trước thành công, trả về thông tin sách sau khi cập nhật.',
                examples=[OpenApiExample(
                    'Thành công',
                    value={'message': 'Stock reserved.', 'book': {'id': 1, 'title': 'Clean Code', 'stock': 5}},
                )],
            ),
            400: OpenApiResponse(description='Không đủ tồn kho.'),
            404: OpenApiResponse(description='Không tìm thấy sách.'),
        },
    )
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
    @extend_schema(
        tags=['Stock Management'],
        summary='Hoàn trả tồn kho sách',
        description=(
            'Tăng số lượng tồn kho của sách khi đơn hàng bị hủy hoặc hoàn trả. '
            'Sử dụng database-level locking để đảm bảo tính nhất quán.'
        ),
        request=StockAdjustSerializer,
        responses={
            200: OpenApiResponse(
                response=BookSerializer,
                description='Hoàn trả thành công, trả về thông tin sách sau khi cập nhật.',
                examples=[OpenApiExample(
                    'Thành công',
                    value={'message': 'Stock released.', 'book': {'id': 1, 'title': 'Clean Code', 'stock': 10}},
                )],
            ),
            404: OpenApiResponse(description='Không tìm thấy sách.'),
        },
    )
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
    @extend_schema(
        tags=['Health'],
        summary='Kiểm tra trạng thái dịch vụ',
        description='Trả về trạng thái hoạt động của Book Service. Dùng cho health check monitoring.',
        responses={
            200: OpenApiResponse(
                description='Dịch vụ đang hoạt động bình thường.',
                examples=[OpenApiExample(
                    'OK',
                    value={'service': 'book-service', 'status': 'ok'},
                )],
            ),
        },
    )
    def get(self, request):
        return Response({'service': 'book-service', 'status': 'ok'})
