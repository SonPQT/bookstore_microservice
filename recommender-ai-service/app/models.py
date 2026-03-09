from django.db import models

class RecommendationRequest(models.Model):
    customer_id = models.PositiveIntegerField()
    strategy = models.CharField(max_length=50, default='top-rated')
    result_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'RecommendationRequest(customer={self.customer_id}, strategy={self.strategy})'
