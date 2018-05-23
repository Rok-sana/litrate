import mysql.connector
from mysql.connector import MySQLConnection, Error


# Класс для работы с БД
class MySqlDatabase:

    def __init__(self, config):
        self.dbconfig = config

    # Выполняет запрос и возвращает результат выполнения в виде словаря
    def execute_query(self, query, multi=False):
        try:
            conn = MySQLConnection(**self.dbconfig)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, multi=multi)

            row = cursor.fetchone()
            result = {}
            while row is not None:
                for key in row.keys():
                    if result.get(key) is None:
                        result[key] = [row[key]]
                    else:
                        result[key].append(row[key])
                row = cursor.fetchone()
            conn.commit()
            return result
        except Error as e:
            print("!!!Error!!!")
            print(query)
            print(e)
            return {}
        finally:
            cursor.close()
            conn.close()

    # Проверяет БД на наличие таблицы
    def check_for_table(self, table_name):
        result = self.all_tables()
        if str(table_name) in result['Tables_in_{0}'.format(self.dbconfig['database'])]:
            return True
        return False

    # Возвращает все таблицы в БД
    def all_tables(self):
        query = "show tables;"
        return self.execute_query(query)



