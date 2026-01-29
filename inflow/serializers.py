from rest_framework import serializers
from inflow.models import InFlow


class InflowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InFlow
        fields = '__all__'
