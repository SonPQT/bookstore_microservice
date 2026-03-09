from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer, ReservePaymentSerializer


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer


class PaymentDetail(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentReserve(APIView):
    def post(self, request):
        serializer = ReservePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if Payment.objects.filter(order_id=data['order_id']).exists():
            return Response({'error': 'Payment for this order already exists.'}, status=status.HTTP_409_CONFLICT)
        payment = Payment.objects.create(**data, status='RESERVED')
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentConfirm(APIView):
    def post(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        if payment.status == 'CANCELLED':
            return Response({'error': 'Cancelled payment cannot be confirmed.'}, status=status.HTTP_400_BAD_REQUEST)
        payment.status = 'CONFIRMED'
        payment.save(update_fields=['status', 'updated_at'])
        return Response(PaymentSerializer(payment).data)


class PaymentCancel(APIView):
    def post(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        payment.status = 'CANCELLED'
        payment.save(update_fields=['status', 'updated_at'])
        return Response(PaymentSerializer(payment).data)


class OrderPayment(APIView):
    def get(self, request, order_id):
        payment = Payment.objects.filter(order_id=order_id).first()
        if not payment:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PaymentSerializer(payment).data)


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'pay-service', 'status': 'ok'})
