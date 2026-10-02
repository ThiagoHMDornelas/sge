from rest_framework import serializers
from outflow.models import OutFlow


class OutflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutFlow
        fields = '__all__'

    def validate(self, attrs):
        product = attrs.get('product', getattr(self.instance, 'product', None))
        quantity = attrs.get('quantity', getattr(self.instance, 'quantity', None))

        if product is None or quantity is None:
            return attrs

        available = product.quantity
        if self.instance and self.instance.product_id == product.pk:
            available += self.instance.quantity

        if quantity > available:
            raise serializers.ValidationError({
                'quantity': f'Estoque insuficiente. Disponível: {available} unidades.'
            })

        return attrs
