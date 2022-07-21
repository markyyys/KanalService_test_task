import psycopg2
from config import host, user, password, db_name, table_name

def connect_to_db():
    # подключение к бд
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    return connection

def table_create():
    try:
        connection = connect_to_db()

        with connection.cursor() as cursor:
            # проверка существует ли таблица
            cursor.execute("SELECT exists (SELECT * from information_schema.tables WHERE table_name=%s)", ('test',))
            if not cursor.fetchone()[0]:
                # создание таблицы
                cursor.execute("""CREATE TABLE {}(
                                  № serial PRIMARY KEY,
                                  заказ_№ integer,
                                  стоимость_в_$ integer,
                                  стоимость_в_руб real,
                                  срок_поставки date)""".format(table_name))

    except Exception as x:
        print("Ошибка создания " + str(x))

    finally:
        if connection:
            connection.close()

def get_table(rows = """ "№", "заказ_№", "стоимость_в_$", "срок_поставки" """):
    # получение записей из бд
    try:
        connection = connect_to_db()

        with connection.cursor() as cursor:
            get_query = """SELECT {} FROM test """.format(rows)
            cursor.execute(get_query)
            table = [list(v) for v in cursor.fetchall()]

    except Exception as x:
        print("Ошибка получения " + str(x))

    finally:
        if connection:
            connection.close()

        return table

def table_update(rates, deleted = [], added = []):
    # обновление записей в бд
    try:
        connection = connect_to_db()

        with connection.cursor() as cursor:
            # удаление
            delete_query = """DELETE FROM test WHERE заказ_№ = %s"""
            cursor.executemany(delete_query, deleted)
            # добавление
            add_query = """INSERT INTO test(№, заказ_№, стоимость_в_$, срок_поставки) VALUES (%s,%s,%s,%s)"""
            cursor.executemany(add_query, added)
            # добавление цены в рублях
            prices = [[list(v)[0] * rates, list(v)[1]] for v in get_table(rows=""" "стоимость_в_$", "№" """)]
            rub_query = """UPDATE test SET стоимость_в_руб = %s WHERE № = %s"""
            cursor.executemany(rub_query, prices)

    except Exception as x:
        print("Ошибка обновления " + str(x))

    finally:
        if connection:
            connection.close()