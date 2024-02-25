from config import MENU_MESSAGE
from data.data import EMPLOYERS_LIST
from db.db_manager import DBManager
from utils.hh import HHParser


def main() -> None:
    """
    Главная функция программы.
    Собирает информацию о компаниях и их вакансиях.
    Записывает собранную информацию в базу данных.
    Предоставляет пользователю интерактивное меню для удобного просмотра собранной информации.
    """
    db = DBManager()
    db_name = "hh"
    db.create_database(db_name=db_name)
    db.create_tables(db_name=db_name)

    hh = HHParser()
    print("Сервис сбора вакансий по списку работодателей")
    print("Собираем информацию, ожидайте")
    employers = hh.get_filtered_employers(EMPLOYERS_LIST)
    print("[+] Собрали информацию о работодателях")
    db.write_data_in_table(db_name=db_name, name_table="employers", data=employers)
    print("[+] Записали информацию о работодателях в БД")
    vacancies_employers = hh.get_all_vacancies(employers)
    filtered_vacancies_employers = hh.get_filtered_vacancies(vacancies_employers)
    print("[+] Собрали информацию о вакансиях")
    db.write_data_in_table(db_name=db_name, name_table="vacancies", data=filtered_vacancies_employers)
    print("[+] Записали информацию о вакансиях в БД")
    print("[+] Сбор информации о вакансиях завершён успешно")
    print("-" * 50)
    while True:
        print(MENU_MESSAGE)
        menu_item = input(">> ")
        if menu_item not in ["0", "1", "2", "3", "4", "5"]:
            print("[!] Ошибка ввода. Выберите пункт из меню")
        if menu_item == "0":
            print("Спасибо что воспользовались программой.")
            quit()
        if menu_item == "1":
            for item in db.get_companies_and_vacancies_count(db_name=db_name):
                print(f"Название компании: {item[0]}\nКоличество вакансий: {item[1]}\nСсылка на компанию: {item[2]}")
                print("-" * 50)
        if menu_item == "2":
            for item in db.get_all_vacancies(db_name=db_name):
                currency = "Не указана" if item[4] is None else f"{item[2]} - {item[3]} {item[4]}"
                print(f"Название компании: {item[0]}\nДолжность: {item[1]}")
                print(f"Зарплата: {currency}\nСсылка на вакансию: {item[-1]}")
                print("-" * 50)
        if menu_item == "3":
            print(f"Средняя зарплата по вакансиям: {db.get_avg_salary(db_name=db_name)}")
        if menu_item == "4":
            for item in db.get_vacancies_with_higher_salary(db_name=db_name):
                currency = "Не указана" if item[4] is None else f"{item[2]} - {item[3]} {item[4]}"
                print(f"Название компании: {item[0]}\nДолжность: {item[1]}")
                print(f"Зарплата: {currency}\nСсылка на вакансию: {item[-1]}")
                print("-" * 50)
        if menu_item == "5":
            while True:
                print('Введите текст для поиска или "1" для возвращения к главному меню или "0"', end=" ")
                print("для выхода из программы")
                search_text = input(">> ")
                if search_text == "0":
                    print("Спасибо что воспользовались программой.")
                    quit()
                if search_text == "1":
                    break
                finded_vacancies = db.get_vacancies_with_keyword(db_name=db_name, search_words=search_text)
                if finded_vacancies:
                    for item in finded_vacancies:
                        currency = "Не указана" if item[4] is None else f"{item[2]} - {item[3]} {item[4]}"
                        print(f"Название компании: {item[0]}\nДолжность: {item[1]}")
                        print(f"Зарплата: {currency}\nОбязанности: {item[-2]}\nСсылка на вакансию: {item[-1]}")
                        print("-" * 50)
                    break
                else:
                    print("По Вашему запросу не было найдено ни одной вакансии")


if __name__ == "__main__":
    main()
