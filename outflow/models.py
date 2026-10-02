from django.core.validators import MinValueValidator
from django.db import models
from core.models import BaseModel

from product.models import Product


class OutFlow(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="outflow_product"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product)
