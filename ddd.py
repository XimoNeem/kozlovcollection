import psycopg2
import dj_database_url

# Получаем строку подключения как словарь
database_config = dj_database_url.config(
    default='postgresql://kozlovcollection:zJYHxV9AGNOr09jfLIJ8AqtDFTVYUF5r@dpg-cu799gin91rc73d1tskg-a.oregon-postgres.render.com/collection_djdh'
)

# Подключаемся к базе данных с использованием полученного словаря
connection = psycopg2.connect(
    dbname=database_config['NAME'],
    user=database_config['USER'],
    password=database_config['PASSWORD'],
    host=database_config['HOST'],
    port=database_config['PORT']
)

# Создаем курсор для выполнения запросов
with connection.cursor() as cursor:
    # Выполним SQL-запрос для удаления всех записей
    cursor.execute("DELETE FROM app_authorpdf;")
    print("Все записи из таблицы app_authorpdf удалены")

# Закрываем соединение
connection.close()
