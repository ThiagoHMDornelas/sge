from django.db.models.signals import post_save
from django.dispatch import receiver

from inflow.models import InFlow


@receiver(post_save, sender=InFlow)
def update_produtct_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            product = instance.product
            product.quantity += instance.quantity
            product.save()
