"""

La idea es la siguiente:
Una martingala en la bolsa que doble la distancia en vez de la apuesta es ligeramente rentable ya que:
Si la accion vale 100 y nosotros estamos buscando el 120 y la perdida seria en 90, hay un 50% de prob
de llegar a cada una, sin embargo una vez llegada la probabilidad de que suba del 110 al 120 es mas cerca que
de 110 a 90

"""
import random


total_money = 0
min_money = 0


def martingala():
    global  min_money
    bet_list = [1]
    money = 0

    while money < 1:
        print(bet_list)
        movimiento = random.randint(0, 1)
        apuesta = min(bet_list)
        indice = bet_list.index(apuesta)

        if movimiento == 0:     # WIN
            money += apuesta
            bet_list.pop(indice)

        else:                   # LOSS
            money -= apuesta
            bet_list[indice] *= 2

            if bet_list[indice] == 16:
                for i in range(int(bet_list[indice]/2)):
                    bet_list.append(2)
                bet_list.pop(indice)

        if money < min_money:
            min_money = money

        if len(bet_list) > 100:
            return money

    return money


for i in range(100000):
    money = martingala()
    total_money += money

print("TOTAL: " + str(total_money))
print("Min: " + str(min_money))





""" pork aqui siempre ganaba?

total_money = 0


def martingala():
    bet_list = [1]
    money = 0

    while money < 1000:
        movimiento = random.randint(0, 1)
        apuesta = min(bet_list)
        indice = bet_list.index(apuesta)

        if movimiento == 0:     # WIN
            money += apuesta
            apuesta = 1

        else:                   # LOSS
            money -= apuesta
            apuesta = apuesta*2

        if apuesta == 16:
            for i in range(int(apuesta/2)):
                bet_list.append(2)
            bet_list.pop(indice)

    return money


for i in range(1):
    money = martingala()
    total_money += money

print("TOTAL: " + str(total_money))
"""