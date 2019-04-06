from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Order
from markets.models import Market
from tickers.models import Ticker
from trades.models import Trade


USER_MODEL = get_user_model()

class Matching():
    @staticmethod
    def get_bid_ask( market : Market):
        bid = market.order_set.filter(side=Order.SIDES_BUY, status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED]).exclude(price=0).order_by("-price")
        ask = market.order_set.filter(side=Order.SIDES_SELL, status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED]).exclude(price=0).order_by("price")
        bid_price = None
        ask_price = None
        if len(bid) > 0:
            bid_price = bid[0].price
        if len(ask) > 0:
            ask_price = ask[0].price

        return (bid_price, ask_price)


    @staticmethod
    def take( order: Order):
        depth = []
        if order.side == Order.SIDES_SELL:
            depth = order.market.order_set.filter(side=Order.SIDES_BUY, status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED]).exclude(price=0).order_by("-price")
        if order.side == Order.SIDES_BUY:
            depth = order.market.order_set.filter(side=Order.SIDES_SELL, status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED]).exclude(price=0).order_by("price")
        for o in depth:
            if (order.side == Order.SIDES_SELL and order.price != 0 and order.price > o.price) or (order.side == Order.SIDES_BUY and order.price != 0 and order.price < o.price):
                break
            if order.size - order.filled > o.size - o.filled:
                fill_size = o.size - o.filled
            else:
                fill_size = order.size - order.filled
            o.fill( fill_size )
            order.fill( fill_size )
            o.save()
            order.save()
            if order.side == Order.SIDES_SELL:
                order_buy = o
                order_sell = order
            else:
                order_buy = order
                order_sell = o


            Trade.objects.create(
                order_buy = order_buy,
                order_sell = order_sell,
                price = o.price,
                side = order.side
            )
            if order.status == Order.STATUS_FILLED:
                break

    @staticmethod
    def process_order(self, order: Order ):
        if order.status == Order.STATUS_WAITING_NEW:
            order.status = Order.STATUS_NEW
            order.save()

#            best_bid_price, best_ask_price = self.get_bid_ask(order.market)
            if order.price == 0:
                Matching.take(order)
                order.status = Order.STATUS_FILLED
                order.save()
            if order.price != 0:
                Matching.take(order)




class TestOrder(TestCase):

    def setUp(self) -> None:
        self.ticker1 = Ticker.objects.create(name="USD")
        self.ticker2 = Ticker.objects.create(name="EUR")
        self.market = Market.objects.create(name="USD/EUR",
                                            base_currency=self.ticker1,
                                            quote_currency=self.ticker2)

        self.Alice = USER_MODEL.objects.create_user(username="Alice", email="alice@yy.ru", password="hhhh")
        self.Bob = USER_MODEL.objects.create_user(username="Bob", email="bob@yy.ru", password="hhhh")

        # Creating Alice orders
        for i in range(20):
            Order.objects.create(sender=self.Alice,
                               side=Order.SIDES_SELL,
                               price=10000 + i*100,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)

        # Creating Alice orders
        for i in range(20):
            Order.objects.create(sender=self.Alice,
                               side=Order.SIDES_BUY,
                               price=10000 - i*100,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)

        # Creating Bob orders
        for i in range(2):
            Order.objects.create(sender=self.Bob,
                               side=Order.SIDES_BUY,
                               price=0,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)


    def test_market_exists(self):
        assert Market.objects.all().count() == 1

    def test_orders_created(self):
        #assert Market.objects.all()[0].order_set.count() == 40
        print("---BID----")
        for order in Market.objects.all()[0].order_set.filter(side=Order.SIDES_BUY).exclude(price=0).order_by("-price", "created_at"):
            print(order.price, order.size)

        print("---ASK----")
        for order in Market.objects.all()[0].order_set.filter(side=Order.SIDES_SELL).exclude(price=0).order_by("price", "created_at"):
            print(order.price, order.size)



    def test_get_level_1(self):
        bid = Market.objects.all()[0].order_set.filter(side=Order.SIDES_BUY, status__in=[Order.STATUS_WAITING_NEW]).exclude(price=0).order_by("-price")
        ask = Market.objects.all()[0].order_set.filter(side=Order.SIDES_SELL, status__in=[Order.STATUS_WAITING_NEW]).exclude(price=0).order_by("price")
        bid_price = None
        ask_price = None
        if len(bid) > 0:
            bid_price = bid[0].price
        if len(ask) > 0:
            ask_price = ask[0].price

        print(f'Bid {bid_price} Ask {ask_price}')

