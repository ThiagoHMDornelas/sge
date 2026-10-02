from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.stock import apply_stock_delta
from outflow.models import OutFlow


@receiver(pre_save, sender=OutFlow)
def capture_previous_state(sender, instance, **kwargs):
    instance._previous = None
    if instance.pk:
        instance._previous = OutFlow.objects.filter(pk=instance.pk).first()


@receiver(post_save, sender=OutFlow)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        apply_stock_delta(instance.product, -instance.quantity)
        return

    previous = instance._previous
    if previous is None:
        return

    if previous.product_id == instance.product_id:
        apply_stock_delta(instance.product, previous.quantity - instance.quantity)
    else:
        apply_stock_delta(previous.product, previous.quantity)
        apply_stock_delta(instance.product, -instance.quantity)


@receiver(post_delete, sender=OutFlow)
def restore_product_quantity(sender, instance, **kwargs):
    apply_stock_delta(instance.product, instance.quantity)
