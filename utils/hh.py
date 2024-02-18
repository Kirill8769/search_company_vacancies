from datetime import datetime

import requests


class HHParser:

    @staticmethod
    def __get_employers(search_query: str = "") -> list | list[dict]:
        """ TEXT """
        employers = []
        params = {"text": search_query, "only_with_vacancies": True, "sort_by": "by_vacancies_open"}
        url = "https://api.hh.ru/employers"
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            employers = response.json()["items"]
        return employers

    @staticmethod
    def __get_employer_info(employer_id: str):
        data = []
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url=url)
        if response.status_code == 200:
            data = response.json()
        return data

    def get_filtered_employers(self, user_employers_data: list | None = None) -> list | list[dict]:
        """ TEXT """
        employers_list = []
        filter_employers_list = []
        if user_employers_data is not None:
            for user_element in user_employers_data:
                employers_list.append(self.__get_employer_info(user_element["id"]))
        else:
            employers_list = self.__get_employers()
        for employer in employers_list:
            filter_employers_list.append({
                "employer_id": employer["id"],
                "name": employer["name"],
                "url": employer["alternate_url"],
                "open_vacancies": employer["open_vacancies"],
            })
        return filter_employers_list

    @staticmethod
    def get_vacancies_employer(employer_id: str) -> list | list[dict]:
        """ TEXT """
        vacancies = []
        params = {"employer_id": employer_id}
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            vacancies = response.json()["items"]
        return vacancies

    def get_all_vacancies(self, employers_list: list):
        all_vacancies = []
        for employer in employers_list:
            vacancies = self.get_vacancies_employer(employer["employer_id"])
            all_vacancies.extend(vacancies)
        return all_vacancies

    @staticmethod
    def get_filtered_vacancies(vacancies_list: list):
        """ TEXT """
        filter_vacancies_list = []
        for vacancy in vacancies_list:
            published_date = datetime.strptime(vacancy["published_at"], "%Y-%m-%dT%H:%M:%S%z")
            if vacancy["salary"] is not None:
                salary = vacancy["salary"]
                salary_from = salary["from"] if salary["from"] is not None else 0
                salary_to = salary["to"] if salary["to"] is not None else 0
                currency = salary["currency"]
            else:
                salary_from = 0
                salary_to = 0
                currency = None
            snippet = vacancy["snippet"]
            description = f"Обязанности: {snippet['requirement']}\nТребования: {snippet['responsibility']}"
            filter_vacancies_list.append(
                {
                    "vacancy_id": vacancy["id"],
                    "employer_id": vacancy["employer"]["id"],
                    "name": vacancy["name"],
                    "status": vacancy["type"]["name"],
                    "published_date": published_date,
                    "url": vacancy["alternate_url"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "description": description,
                }
            )
        return filter_vacancies_list
