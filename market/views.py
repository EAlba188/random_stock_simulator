from django.views import View
from django.template.response import TemplateResponse
from .models import UserModel, StockModel, PriceModel, StockOwnedModel
from django.http import JsonResponse
from django.db.models import Max
from django.shortcuts import render, redirect
from .price_movement import iniciar_accion_periodica
import json


class MarketView(View):
    template = "market.html"
    iniciar_accion_periodica()
    #precio_maximo = PriceModel.objects.aggregate(max_valor=Max('price'))['max_valor'] # TODO Ojo a este metodo para sacar el mayor valor

    def get(self, request):
        stocks_owned = StockOwnedModel.objects.first()
        user_selected = UserModel.objects.first()
        stock = StockModel.objects.first()

        return TemplateResponse(request, self.template, {
            "user_selected": user_selected,
            "stock": stock,
            "owned": stocks_owned.number,
            "buy_price": stocks_owned.buy_price,
        })

    def post(self, request):
        stocks_owned = StockOwnedModel.objects.first()
        user_selected = UserModel.objects.first()
        action = request.GET.get("action")
        amount_buy = request.POST.get("amount-buy", None)
        amount_sell = request.POST.get("amount-sell", None)
        stock = StockModel.objects.first()

        if action == "buy-all":
            action = "buy"
            amount_buy = int(user_selected.money/stock.last_price)

        if action == "sell-all":
            if stocks_owned.number > 0:
                action = "sell"
                amount_sell = int(stocks_owned.number)

        if action == "buy":
            stocks_owned.buy_price = (int(amount_buy)*int(stock.last_price)\
                                          +int(stocks_owned.number)*int(stocks_owned.buy_price))\
                                          /(int(stocks_owned.number)+int(amount_buy))
            user_selected.money -= int(amount_buy)*int(stock.last_price)
            stocks_owned.number += int(amount_buy)

        elif action == "sell":
            user_selected.money += int(amount_sell)*int(stock.last_price)
            stocks_owned.number -= int(amount_sell)
            if stocks_owned.number == 0:
                stocks_owned.buy_price = 0

        user_selected.save()
        stocks_owned.save()

        return TemplateResponse(request, self.template, {
            "user_selected": user_selected,
            "stock": stock,
            "owned": stocks_owned.number,
            "buy_price": stocks_owned.buy_price,
        })


class LastPricesView(View):

    def get(self, request):
        last_prices = PriceModel.objects.order_by("-created_at")[:100]
        last_prices_list = []

        for price in last_prices:
            last_prices_list.insert(0, price.price)

        data = dict()
        data["data"] = last_prices_list

        return JsonResponse(data)


class RestartView(View):
    def get(self, request):
        user_selected = UserModel.objects.first()
        stocks_owned = StockOwnedModel.objects.first()
        stock = StockModel.objects.first()
        PriceModel.objects.all().delete()

        user_selected.money = 1000
        user_selected.save()
        stocks_owned.number = 0
        stocks_owned.buy_price = 0
        stocks_owned.save()
        stock.last_price = 150
        stock.save()

        return redirect("market")

# TODO lista de add shit
# Velocidad de la accion (cambiar la frecuencia del thread y de actualizacion)
# Vista movil, que se actualice segun minimo y maximo del grafico
# Ver mas, mas de 20 movimientos