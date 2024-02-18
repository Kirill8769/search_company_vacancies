from config import EMPLOYERS_LIST
from utils.hh import HHParser


def main():
    hh = HHParser()
    employers = hh.get_filtered_employers(EMPLOYERS_LIST)
    print(employers)
    print(len(employers))
    vacancies_employers = hh.get_all_vacancies(employers)
    filtered_vacancies_employers = hh.get_filtered_vacancies(vacancies_employers)
    #
    for com in employers:
        print(com)
        break

    for vac in filtered_vacancies_employers:
        print(vac)
        break


if __name__ == "__main__":
    main()
