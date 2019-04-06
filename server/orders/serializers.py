from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderUser(serializers.ModelSerializer):

    signature = serializers.CharField()
    market = serializers.CharField()

    class Meta:
        model = Order
        fields = ('sender',
                  'signature',
                  'market',
                  'size',
                  'price',
                  'hash_signature')
