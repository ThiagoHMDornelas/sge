from rest_framework import serializers
from outflow.models import OutFlow


class OutflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutFlow
        fields = '__all__'
