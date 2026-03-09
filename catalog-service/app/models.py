from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    keyword = models.CharField(max_length=120, blank=True)
    featured_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
