import os
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer

CART_SERVICE_URL = os.getenv('CART_SERVICE_URL', 'http://cart-service:8000')


class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        try:
            response = requests.post(
                f'{CART_SERVICE_URL}/carts/',
                json={'customer_id': customer.id},
                timeout=5,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            customer.delete()
            return Response(
                {
                    'error': 'Customer created but cart creation failed. Customer was rolled back.',
                    'details': str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Customer created and cart initialized successfully.',
                'customer': CustomerSerializer(customer).data,
                'cart': response.json(),
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CustomerDetail(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'customer-service', 'status': 'ok'})
