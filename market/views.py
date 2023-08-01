from django.views import View
from django.template.response import TemplateResponse
from .models import UserModel, StockModel, PriceModel
from django.http import JsonResponse
from django.db.models import Max
from .price_movement import iniciar_accion_periodica
import json


class MarketView(View):
    template = "market.html"
    user_selected = UserModel.objects.first()
    stock = StockModel.objects.first()
    iniciar_accion_periodica()
    #precio_maximo = PriceModel.objects.aggregate(max_valor=Max('price'))['max_valor'] # TODO Ojo a este metodo para sacar el mayor valor

    def get(self, request):

        return TemplateResponse(request, self.template, {
            "user_selected": self.user_selected,
            "stock": self.stock,
        })

    def post(self, request):
        action = request.GET.get("action")
        if action == "buy":
            amount = request.POST.get("amount-buy")
        else:
            amount = request.POST.get("amount-sell")

        return TemplateResponse(request, self.template, {
            "user_selected": self.user_selected,
            "stock": self.stock,
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