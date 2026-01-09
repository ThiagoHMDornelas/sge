from django.db import models
from core.models import BaseModel
from django.db.models.functions import Lower

from category.models import Category
from brands.models import Brand


class Product(BaseModel):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="product_category")
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="product_brand")
    serie_number = models.CharField(max_length=100, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = [Lower("name")]

    def __str__(self):
        return self.name
