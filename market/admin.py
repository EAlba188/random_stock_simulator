from django.contrib import admin

from .models import UserModel
from .models import StockModel

admin.site.register(UserModel)
admin.site.register(StockModel)