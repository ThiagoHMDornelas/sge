from django.db import models
from django.conf import settings

from supplier.models import Supplier
from product.models import Product


class InFlows(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inflow_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inflow_updated"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product)
