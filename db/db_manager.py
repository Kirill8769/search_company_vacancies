import os

import psycopg2

from config import PATH_PROJECT
from db.db_config import config


class DBManager:

    def __init__(self):
        self.__params = config()

    def create_database(self, db_name: str) -> None:
        """
        Метод пересоздаёт базу данных.

        :param db_name: Имя базы данных.
        """
        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        with conn.cursor() as cur:
            script = f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}' -- ← изменить на свое название БД
                AND pid <> pg_backend_pid();
            """
            cur.execute(script)
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        conn.close()

    def connect_db(self, db_name: str) -> psycopg2.extensions.connection:
        """
        Метод подключается к базе данных.

        :param db_name: Имя базы данных.
        :return: Коннектор для дальнейшей работы в БД.
        """
        connector = psycopg2.connect(dbname=db_name, **self.__params)
        connector.autocommit = True
        return connector

    def execute_query(self, db_name: str, query: str) -> list | list[tuple]:
        """
        Метод делает запрос к базе данных.

        :param db_name: Имя базы данных.
        :param query: Запрос.
        :return: Результат запроса.
        """
        connector = self.connect_db(db_name=db_name)
        connector.autocommit = True
        with connector.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        connector.close()
        return result

    def create_tables(self, db_name: str) -> None:
        """
        Метод создаёт таблицы в БД.

        :param db_name: Имя базы данных.
        """
        script_path = os.path.join(PATH_PROJECT, "db", "create_tables.sql")
        with open(script_path, encoding="UTF-8") as file:
            script = file.read()
        conn = self.connect_db(db_name=db_name)
        with conn.cursor() as cur:
            cur.execute(script)
        conn.close()

    def write_data_in_table(self, db_name: str, name_table: str, data: list[dict]) -> None:
        """
        Метод записывает данные в БД.

        :param db_name: Имя базы данных
        :param name_table: Имя таблицы
        :param data: Список с данными
        """
        conn = self.connect_db(db_name=db_name)
        with conn.cursor() as cur:
            values_len = "%s, " * len(data[0].keys())
            file_column = ", ".join(data[0].keys())
            insert_data = (tuple(item.values()) for item in data)
            cur.executemany(f"""
                INSERT INTO {name_table} ({file_column})
                VALUES ({values_len[:-2]})
                ON CONFLICT ({file_column.split(",")[0]}) DO NOTHING
            """, insert_data,)

    def get_companies_and_vacancies_count(self, db_name: str) -> list | list[tuple]:
        """
        Метод получает список всех компаний и количество вакансий у каждой компании.

        :param db_name: Имя базы данных.
        :return: Список всех компаний и количество вакансий у каждой компании.
        """
        query = "SELECT name, open_vacancies, url FROM employers ORDER BY 2 DESC"
        result_query = self.execute_query(db_name=db_name, query=query)
        return result_query

    def get_all_vacancies(self, db_name: str) -> list | list[tuple]:
        """
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.

        :param db_name: Имя базы данных.
        :return: Список всех вакансий с краткой информацией о них.
        """
        query = """
            SELECT e.name, v.name, salary_from, salary_to, currency, v.url
            FROM employers e
                JOIN vacancies v USING(employer_id)
            ORDER BY 1, 2
        """
        result_query = self.execute_query(db_name=db_name, query=query)
        return result_query

    def get_avg_salary(self, db_name: str) -> int:
        """
        Метод получает среднюю зарплату по вакансиям.

        :param db_name: Имя базы данных.
        :return: Средний размер ЗП по вакансиям в БД.
        """
        conn = self.connect_db(db_name=db_name)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ROUND(AVG(salary_from + salary_to)) as avg_salary
                FROM vacancies
                WHERE salary_from > 0 AND salary_to > 0
            """)
            result = cur.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self, db_name: str) -> list | list[tuple]:
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :param db_name: Имя базы данных.
        :return: Список всех вакансий, у которых зарплата выше средней.
        """
        avg_salary = self.get_avg_salary(db_name=db_name)
        query = f"""
            SELECT e.name, v.name, salary_from, salary_to, currency, v.url
            FROM vacancies v
                JOIN employers e USING(employer_id)
            WHERE salary_from > {avg_salary}
        """
        result_query = self.execute_query(db_name=db_name, query=query)
        return result_query

    def get_vacancies_with_keyword(self, db_name: str, search_words: str) -> list | list[tuple]:
        """
        Метод получает список всех вакансий по переданному тексту.

        :param db_name: Имя базы данных.
        :param search_words: Текст для поиска.
        :return: Список найденных вакансий.
        """
        query = f"""
            SELECT e.name, v.name, salary_from, salary_to, currency, description, v.url
            FROM vacancies v
                JOIN employers e USING(employer_id)
            WHERE v.name LIKE '%{search_words.lower()}%'
                OR v.name LIKE '%{search_words.capitalize()}%'
        """
        result_query = self.execute_query(db_name=db_name, query=query)
        return result_query
