import os
import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Staff
from .serializers import StaffSerializer

BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')


class StaffListCreate(generics.ListCreateAPIView):
    queryset = Staff.objects.all().order_by('id')
    serializer_class = StaffSerializer


class StaffDetail(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffBookProxy(APIView):
    def get(self, request):
        response = requests.get(f'{BOOK_SERVICE_URL}/books/', timeout=5)
        return Response(response.json(), status=response.status_code)

    def post(self, request):
        response = requests.post(f'{BOOK_SERVICE_URL}/books/', json=request.data, timeout=5)
        return Response(response.json(), status=response.status_code)


class StaffBookProxyDetail(APIView):
    def get(self, request, book_id):
        response = requests.get(f'{BOOK_SERVICE_URL}/books/{book_id}/', timeout=5)
        return Response(response.json(), status=response.status_code)

    def put(self, request, book_id):
        response = requests.put(f'{BOOK_SERVICE_URL}/books/{book_id}/', json=request.data, timeout=5)
        return Response(response.json(), status=response.status_code)

    def patch(self, request, book_id):
        response = requests.patch(f'{BOOK_SERVICE_URL}/books/{book_id}/', json=request.data, timeout=5)
        return Response(response.json(), status=response.status_code)

    def delete(self, request, book_id):
        response = requests.delete(f'{BOOK_SERVICE_URL}/books/{book_id}/', timeout=5)
        body = {}
        try:
            body = response.json()
        except Exception:
            body = {'message': 'Book deleted.'}
        return Response(body, status=response.status_code)


class HealthView(APIView):
    def get(self, request):
        return Response({'service': 'staff-service', 'status': 'ok'})
