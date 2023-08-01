from django.contrib import admin
from django.urls import path
from market.views import MarketView, LastPricesView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("market/", MarketView.as_view(), name="market"),
    path("last_prices/", LastPricesView.as_view(), name="last_prices"),
]
