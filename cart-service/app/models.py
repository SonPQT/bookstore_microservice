from django.db import models

class Cart(models.Model):
    customer_id = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart(customer_id={self.customer_id})'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'book_id'], name='unique_book_per_cart')
        ]

    def __str__(self):
        return f'CartItem(cart={self.cart_id}, book={self.book_id}, qty={self.quantity})'
