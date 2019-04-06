from  rest_framework import serializers
from .models import Market


class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market
        fields = ('name',
                  'smart_contract_address',
                  'base_currency',
                  'quote_currency',

                  'last_price',
                  'max_24_price',
                  'min_24_price',
                  'volume_24',
                  'change_24',
        )
