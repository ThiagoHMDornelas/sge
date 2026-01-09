from django.db import models
from core.models import BaseModel
from django.db.models.functions import Lower


class Supplier(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = [Lower("name")]

    def __str__(self):
        return self.name
