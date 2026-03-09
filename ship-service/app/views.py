from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Shipment
from .serializers import ReserveShipmentSerializer, ShipmentSerializer


class ShipmentList(generics.ListAPIView):
    queryset = Shipment.objects.all().order_by('-id')
    serializer_class = ShipmentSerializer


class ShipmentDetail(generics.RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class ShipmentReserve(APIView):
    def post(self, request):
        serializer = ReserveShipmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if Shipment.objects.filter(order_id=data['order_id']).exists():
            return Response({'error': 'Shipment for this order already exists.'}, status=status.HTTP_409_CONFLICT)
        shipment = Shipment.objects.create(**data, status='RESERVED')
        return Response(ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED)


class ShipmentConfirm(APIView):
    def post(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
        except Shipment.DoesNotExist:
            return Response({'error': 'Shipment not found.'}, status=status.HTTP_404_NOT_FOUND)
        if shipment.status == 'CANCELLED':
            return Response({'error': 'Cancelled shipment cannot be confirmed.'}, status=status.HTTP_400_BAD_REQUEST)
        shipment.status = 'CONFIRMED'
        shipment.save(update_fields=['status', 'updated_at'])
        return Response(ShipmentSerializer(shipment).data)


class ShipmentCancel(APIView):
    def post(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
        except Shipment.DoesNotExist:
            return Response({'error': 'Shipment not found.'}, status=status.HTTP_404_NOT_FOUND)
        shipment.status = 'CANCELLED'
        shipment.save(update_fields=['status', 'updated_at'])
        return Response(ShipmentSerializer(shipment).data)


class OrderShipment(APIView):
    def get(self, request, order_id):
        shipment = Shipment.objects.filter(order_id=order_id).first()
        if not shipment:
            return Response({'error': 'Shipment not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ShipmentSerializer(shipment).data)


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'ship-service', 'status': 'ok'})
