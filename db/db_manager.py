import os

import psycopg2

from config import PATH_PROJECT
from db.db_config import config


class DBManager:

    def __init__(self):
        self.__params = config()

    def connect_db(self) -> psycopg2.extensions.connection:
        """
        Метод для подключения к базе данных.

        :return: Коннектор для соединения с базой данных.
        """
        connector = psycopg2.connect(**self.__params)
        connector.autocommit = True
        return connector

    def create_tables(self) -> None:
        """ Метод создаёт таблицы в БД. """

        conn = self.connect_db()
        script_path = os.path.join(PATH_PROJECT, "db", "create_tables.sql")
        with conn.cursor() as cur:
            with open(script_path, encoding="UTF-8") as file:
                cur.execute(file.read())

    def write_data_in_table(self, name_table: str, data: list[dict]):
        """
        Метод записывает данные в БД.

        :param name_table: Имя таблицы
        :param data: Список с данными
        :return:
        """
        conn = self.connect_db()
        with conn.cursor() as cur:
            values_len = "%s, " * len(data[0].keys())
            file_column = ", ".join(data[0].keys())
            insert_data = (tuple(item.values()) for item in data)
            print(insert_data)
            print(values_len[:-2])
            cur.executemany(f"""
                INSERT INTO {name_table} ({file_column})
                VALUES ({values_len[:-2]})
                ON CONFLICT ({file_column.split(",")[0]}) DO NOTHING
            """, insert_data)

    def get_companies_and_vacancies_count(self):
        """
        Метод получает список всех компаний и количество вакансий у каждой компании.

        :return:
        """

    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

        :return:
        """

    def get_avg_salary(self):
        """
        Метод получает среднюю зарплату по вакансиям.

        :return:
        """

    def get_vacancies_with_higher_salary(self):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return:
        """

    def get_vacancies_with_keyword(self):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

        :return:
        """