from django.views import View
from django.template.response import TemplateResponse
from .models import UserModel, StockModel, PriceModel, StockOwnedModel
from django.http import JsonResponse
from django.db.models import Max
from .price_movement import iniciar_accion_periodica
import json


class MarketView(View):
    template = "market.html"
    user_selected = UserModel.objects.first()
    stocks_owned = StockOwnedModel.objects.first()
    iniciar_accion_periodica()
    #precio_maximo = PriceModel.objects.aggregate(max_valor=Max('price'))['max_valor'] # TODO Ojo a este metodo para sacar el mayor valor

    def get(self, request):
        stock = StockModel.objects.first()

        return TemplateResponse(request, self.template, {
            "user_selected": self.user_selected,
            "stock": stock,
            "owned": self.stocks_owned.number,
            "buy_price": self.stocks_owned.buy_price,
        })

    def post(self, request):
        action = request.GET.get("action")
        stock = StockModel.objects.first()
        if action == "buy":
            amount = request.POST.get("amount-buy")
            self.stocks_owned.buy_price = (int(amount)*int(stock.last_price)\
                                          +int(self.stocks_owned.number)*int(self.stocks_owned.buy_price))\
                                          /(int(self.stocks_owned.number)+int(amount))
            self.user_selected.money -= int(amount)*int(stock.last_price)
            self.stocks_owned.number += int(amount)

        else:
            amount = request.POST.get("amount-sell")
            self.user_selected.money += int(amount)*int(stock.last_price)
            self.stocks_owned.number -= int(amount)
            if self.stocks_owned.number == 0:
                self.stocks_owned.buy_price = 0

        self.user_selected.save()
        self.stocks_owned.save()

        return TemplateResponse(request, self.template, {
            "user_selected": self.user_selected,
            "stock": stock,
            "owned": self.stocks_owned.number,
            "buy_price": self.stocks_owned.buy_price,
        })


class LastPricesView(View):

    def get(self, request):
        last_prices = PriceModel.objects.order_by("-created_at")[:20]
        last_prices_list = []

        for price in last_prices:
            last_prices_list.insert(0, price.price)

        data = dict()
        data["data"] = last_prices_list

        return JsonResponse(data)