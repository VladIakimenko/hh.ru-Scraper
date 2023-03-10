import os
import sys
import json

from scraper import Scraper
from config import RESULT, HOST, URL


def parse(soup):
    def clear_string(object_):
        string = ''.join([c for c in object_.text.replace('\xa0', ' ') if c == ' ' or c.isalnum()])
        return string

    result = []
    vacancies = soup.find_all(class_='vacancy-serp-item__layout')

    for vacancy in vacancies:
        link = vacancy.find(class_='serp-item__title')['href']

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary = clear_string(salary) if salary else ''

        company = vacancy.find(class_='vacancy-serp-item__meta-info-company')
        company = clear_string(company) if company else ''

        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
        city = clear_string(city) if company else ''

        stack = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
        stack = stack.text if stack else ''

        competence = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
        competence = competence.text if competence else ''

        result.append(
            {'link': link,
             'salary': salary,
             'company': company,
             'city': city,
             'stack': stack,
             'competence': competence}
        )
    return result


def save_result(result):
    path = RESULT.replace('\\', '/').rpartition('/')[0]
    if not os.path.exists(path):
        os.makedirs(path)
    with open(RESULT, 'wt', encoding='UTF-8') as output:
        json.dump(result, fp=output)
    print(f'Vacancies saved at: {RESULT}')


def receive_top_20(scraper):
    scraper.requests_get(URL)
    soup = scraper.get_soup()

    vacancies = parse(soup)
    return vacancies


def receive_all(scraper):
    link = URL
    vacancies = []

    while True:
        scraper.driver_get(link)
        soup = scraper.get_soup()
        vacancies += parse(soup)
        next_button = soup.find("a", {'data-qa': 'pager-next'})
        if next_button:
            link = HOST + next_button['href']
        else:
            return vacancies
            
            
def filter_results(vacancies, filters):
    result = []
    if any(filters):
        for vacancy in vacancies:
            for filter_ in filters:
                check_list = [word.lower().strip() for value in vacancy.values() for word in value.split()]
                if filter_.lower().strip() in check_list:
                    result.append(vacancy)
                    break
    else:
        result = vacancies
    return result


if __name__ == '__main__':
    scraper = Scraper()

    print('Choose an option:\n'
          '\t1. Parse top 20\n'
          '\t2. Parse everything')
    while True:
        choice = input().lower().strip()
        if choice in ('1', '2', 'q'):
            break
    if choice == 'q':
        sys.exit()

    print('Choose filters (one line, separate with commas):')
    filters = [filter_.strip() for filter_ in input().split(',')]
    if ''.join(filters):
        print(f'''Only results containing "{'", "'.join(filters)}" will be saved.''')
    else:
        print('No filters will be applied')

    vacancies = (receive_top_20, receive_all)[choice == '2'](scraper)
    vacancies = filter_results(vacancies, filters)
    save_result(vacancies)
