from datetime import datetime
from time import sleep
import requests
from config import bot_token

url = "https://api.telegram.org/bot{}/".format(bot_token)

def send_messages(orders):
    text = []
    # проверка дат поставки
    for o in orders:
        delta = (o[-1] - datetime.now().date()).days
        if delta == 0:
            text.append("Сегодня (" + str(o[-1]) + ") срок поставки заказа № " + str(o[0]))
        elif delta < 0:
            text.append("Заказ № " + str(o[0]) + " просрочен на " + str(abs(delta)) + " дней")
    # отправка сообщений
    for t in text:
        params = {'chat_id': "-1001511075053", 'text': t}
        requests.post(url + 'sendMessage', data=params)
        sleep(1)