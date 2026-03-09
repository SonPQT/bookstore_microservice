from django.db import models

class Review(models.Model):
    customer_id = models.PositiveIntegerField()
    book_id = models.PositiveIntegerField()
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer_id', 'book_id'], name='unique_customer_book_review')
        ]

    def __str__(self):
        return f'Review(customer={self.customer_id}, book={self.book_id}, rating={self.rating})'
