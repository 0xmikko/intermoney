from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    market_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'market',
            'market_display',
            'order_type',
            'side',
            'price',
            'size',
            'filled',
            'status',
            'hash_signature'
        )
        read_only_fields = ('order_type', 'market_display', 'status', 'filled', 'side')

    def get_market_display(self, obj):
        return str(obj.market)


class OrderMake(serializers.ModelSerializer):
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
