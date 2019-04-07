from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    market_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_market_display(self, obj):
        return str(obj.market)

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
