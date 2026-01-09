from django.db import models
from core.models import BaseModel

from supplier.models import Supplier
from product.models import Product


class InFlow(BaseModel):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="inflow_supplier"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="inflow_product"
    )
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product)
