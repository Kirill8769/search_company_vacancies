from data.data import EMPLOYERS_LIST
from db.db_manager import DBManager
from utils.hh import HHParser


def main():
    db = DBManager()
    db.create_database(db_name="hh")
    db.create_tables(db_name="hh")

    hh = HHParser()
    employers = hh.get_filtered_employers(EMPLOYERS_LIST)
    db.write_data_in_table(db_name="hh", name_table="employers", data=employers)
    vacancies_employers = hh.get_all_vacancies(employers)
    filtered_vacancies_employers = hh.get_filtered_vacancies(vacancies_employers)
    db.write_data_in_table(db_name="hh", name_table="vacancies", data=filtered_vacancies_employers)

    print(db.get_vacancies_with_keyword(db_name="hh", search_words="python"))
    print(db.get_vacancies_with_higher_salary(db_name="hh"))
    print(db.get_all_vacancies(db_name="hh"))
    print(db.get_companies_and_vacancies_count(db_name="hh"))
    print(db.get_avg_salary(db_name="hh"))


if __name__ == "__main__":
    main()
