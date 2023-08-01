import threading
import time
from .models import StockModel, PriceModel
import random


def accion_periodica():
    while True:
        stock = StockModel.objects.first()
        movement = random.randint(-10, 10)
        stock.last_price += movement
        stock.save()
        PriceModel.objects.create(price=stock.last_price, stock_related=stock)
        time.sleep(0.02)


def iniciar_accion_periodica():
    thread = threading.Thread(target=accion_periodica)
    thread.daemon = True  # Esto permite que el hilo se detenga cuando el programa principal finalice
    thread.start()
