from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer_id = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=255, blank=True)
    payment_id = models.PositiveIntegerField(null=True, blank=True)
    shipment_id = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - customer {self.customer_id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book_id = models.PositiveIntegerField()
    title_snapshot = models.CharField(max_length=255)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'OrderItem(order={self.order_id}, book={self.book_id}, qty={self.quantity})'
