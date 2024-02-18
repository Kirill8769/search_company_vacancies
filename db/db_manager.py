import psycopg2


class DBManager:

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