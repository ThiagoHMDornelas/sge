from django.db.models import F

from product.models import Product


def apply_stock_delta(product, delta):
    """
    Aplica um delta (positivo ou negativo) na quantidade em estoque do produto.
    Usa F() para atualizar de forma atômica, sem risco de condição de corrida.
    """
    if delta == 0:
        return

    Product.objects.filter(pk=product.pk).update(quantity=F('quantity') + delta)
