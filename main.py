from time import sleep
from db import table_create, table_update, get_table
from sheets import check_updated, get_deleted, get_added_updated
import datetime
from pycbrf.toolbox import ExchangeRates
from telegram import send_messages

def main():
    now = None
    table_create()
    rates = ExchangeRates(str(datetime.datetime.now().date()))

    while True:
        # проверка на обновление таблицы Гугла
        if check_updated():
            table = get_table()
            deleted = get_deleted(table)
            added = get_added_updated(table)
            table_update(rates["USD"].value, deleted=deleted, added=added)
        # каждодневная проверка
        if now != datetime.datetime.now().date():
            now = datetime.datetime.now().date()
            rates = ExchangeRates(str(now)) # обновление курса доллара
            orders = get_table(""" "заказ_№", "срок_поставки" """)
            send_messages(orders) # отправка сообщений тг ботом
        sleep(20)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()