import uuid
from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ('RESERVED', 'Reserved'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_id = models.PositiveIntegerField(unique=True)
    customer_id = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RESERVED')
    provider_reference = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment(order={self.order_id}, status={self.status})'
