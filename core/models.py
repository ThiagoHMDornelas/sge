from django.db import models
from django.conf import settings
from .middleware import get_current_user


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created",
        editable=False,
        null=True,
        blank=True
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_updated",
        editable=False,
        null=True,
        blank=True
    )

    """

    related_name="%(app_label)s_%(class)s_created"
    Isso cria nomes únicos e dinâmicos para cada model:

    MODEL       RELATED_NAME GERADO         USO
    Brand       brands_brand_created        user.brands_brand_created.all()
    Product     products_product_created    user.products_product_created.all()

    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            if not self.pk:  # ← Se NÃO tem PK = está criando
                self.user_created = user
            self.user_updated = user

        super().save(*args, **kwargs)
