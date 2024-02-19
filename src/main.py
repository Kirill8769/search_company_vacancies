from data.data import EMPLOYERS_LIST
from db.db_manager import DBManager
from utils.hh import HHParser


def main():
    db = DBManager()
    print(db.get_vacancies_with_keyword("python"))
    # print(db.get_vacancies_with_higher_salary())
    # print(db.get_all_vacancies())
    # db.get_companies_and_vacancies_count()


    # db.create_tables()
    #
    # hh = HHParser()
    # employers = hh.get_filtered_employers(EMPLOYERS_LIST)
    # db.write_data_in_table("employers", employers)
    # vacancies_employers = hh.get_all_vacancies(employers)
    # filtered_vacancies_employers = hh.get_filtered_vacancies(vacancies_employers)
    # db.write_data_in_table("vacancies", filtered_vacancies_employers)


if __name__ == "__main__":
    main()
