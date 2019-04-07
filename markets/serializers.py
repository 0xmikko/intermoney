from  rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):

    base_currency_display = serializers.SerializerMethodField()
    quote_currency_display = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ('name',
                  'smart_contract_address',
                  'base_currency',
                  'base_currency_display',
                  'quote_currency',
                  'quote_currency_display',
                  'last_price',
                  'max_24_price',
                  'min_24_price',
                  'volume_24',
                  'change_24')


    def get_base_currency_display(self, object):
        return str(object.base_currency)

    def get_quote_currency_display(self, object):
        return str(object.quote_currency)
