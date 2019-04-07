from rest_framework import serializers
from .models import Trade


class TradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ('price', 'size', 'created_at')
