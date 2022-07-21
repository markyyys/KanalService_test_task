from time import sleep
import gspread
from config import CREDENTIALS_FILE, sheet_name
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# подключение к Гуглу
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
# время последнего обновления
time = None # равен None чтобы таблица заполнялась после создания
# таблица из гугла
new_sheet = []

def get_sheet():
    # получение таблицы из Гугла
    global new_sheet
    for i in range(0, 10):
        try:
            new_sheet = client.open(sheet_name).get_worksheet(0).get_all_records()
        except Exception as e: # если привышена квота на запросы то программа ждет
            print(e)
            sleep(4 ** i)
        finally:
            new_sheet = [list(v.values()) for v in new_sheet]
            for s in new_sheet:
                s[-1] = datetime.strptime(s[-1], '%d.%m.%Y').date() # преобразование даты
            return new_sheet
    raise SystemError

def check_updated():
    # проверка обновление таблицы в гугле
    global time
    _time = client.open(sheet_name).lastUpdateTime # временная переменная чтобы не спамить Гугл запросами
    if time != _time:
        time = _time
        get_sheet()
        return True
    else:
        return False

def get_deleted(old):
    # получение удаленных строк с таблицы
    deleted = [[x[1]] for x in old if x not in new_sheet] # возвращает только номера заказов
    return deleted

def get_added_updated(old):
    # получение добавленных строк
    added = [x for x in new_sheet if x not in old]
    return added
