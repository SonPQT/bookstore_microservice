import uuid
from django.db import models

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('RESERVED', 'Reserved'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.PositiveIntegerField(unique=True)
    customer_id = models.PositiveIntegerField()
    method = models.CharField(max_length=30)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RESERVED')
    tracking_code = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Shipment(order={self.order_id}, status={self.status})'
