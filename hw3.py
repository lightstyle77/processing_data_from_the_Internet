import json
import pickle
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""


def scan_hh(vacancy, vacancy_num, vacancy_salary):
    def price_processing(p):
        p = p.replace(" ", "")
        currency = ""
        while not p[-1].isdigit():
            currency = p[-1] + currency
            p = p[:-1]
        if p[0] == "о":
            min_price = int(p[2:])
            max_price = "-"
        elif p[0] == "д":
            max_price = int(p[2:])
            min_price = "-"
        else:
            p = p.split("–")
            min_price = int(p[0])
            max_price = int(p[1])
        result = {
            "min_price": min_price,
            "max_price": max_price,
            "currency": currency
        }
        return result

    def save_pickle(data, path):
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f'Pickle file saved: {path}')

    def load_pickle(path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def save_json(data, file):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Json file saved: {file}")

    def get(url_, headers_, params_):
        result = requests.get(url_, headers=headers_, params=params_)
        return result

    if vacancy_salary == "да":
        vacancy_salary = "true"
    elif vacancy_salary == "нет":
        vacancy_salary = "false"
    else:
        print("Введен некорректный ответ, будут показаны все результаты.")
        vacancy_salary = "false"

    url = "https://hh.ru/search/vacancy"
    params = {
        "text": vacancy,
        "only_with_salary": vacancy_salary,
        "page": 0
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.96 Safari/537.36"
    }

    items_info = list()
    page = 0

    while True:
        my_request = get(url, headers, params)
        soup = bs(my_request.text, "html.parser")
        items = soup.find_all(attrs={"class": "vacancy-serp-item"})
        for item in items:
            info = dict()
            found_item = item.find("a", attrs={"class": "bloko-link"})
            info["href"] = found_item["href"]
            info["name"] = found_item.text
            info["city"] = item.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text

            found_item = item.find("a", attrs={"class": "bloko-link bloko-link_secondary"})
            company = found_item.text.replace("\xa0", " ")
            info["company"] = company

            if item.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"}) is None:
                info["currency"] = "-"
                info["min_salary"] = "-"
                info["max_salary"] = "-"
            else:
                price = item.find(attrs={"class": "vacancy-serp-item__sidebar"}).text.replace("\u202f", " ")
                price = price_processing(price)
                info["currency"] = price["currency"]
                info["min_salary"] = price["min_price"]
                info["max_salary"] = price["max_price"]
            info["get_from"] = my_request.url
            items_info.append(info)

        if page < (vacancy_num - 1):
            page += 1
            params["page"] = page
        else:
            break

    print("----- Scan Done! -----\n")

    return items_info


def databace_update(vacancy, items_info):
    client = MongoClient('localhost', 27017)
    db = client['Job_search']
    collection_name = vacancy.replace(" ", "_")
    collection = db[collection_name]

    for elem in items_info:
        collection.update_one(
            {"href": elem["href"]},
            {"$set": elem},
            upsert=True
        )
    print(f'----- Job_search databace updating completed! Collection name: {vacancy} -----\n')


def databace_search(min_salary, max_salary, vacancy):
    client = MongoClient('localhost', 27017)
    db = client['Job_search']
    collection_name = vacancy.replace(" ", "_")
    collection = db[collection_name]
    if max_salary == "-":
        result = collection.find({
            "min_salary": {"$gte": min_salary}
        })
    else:
        result = collection.find({"$and": [
            {"min_salary": {"$gte": min_salary}},
            {"max_salary": {"$lte": max_salary}}
        ]})
    for item in result:
        pprint(item)


vac = input("Введите вакансию: ")
vac_num = int(input("Введите количество обрабатываемых страниц: "))
vac_salary = input("Обязательно указание ЗП? (да/нет) ").lower()

scan_result = scan_hh(vac, vac_num, vac_salary)

decide = input("Сбор данных завершен. Создать/Обновить базу данных? (да/нет) ")
if decide == "да":
    databace_update(vac, scan_result)
else:
    print(f'----- Database update canceled. -----')

decide = input("Выполнить поиск вакансий по ЗП? (да/нет) ")
if decide == "да":
    decide = input("Выполнить поиск c учетом максимальной ЗП? (да/нет) ")
    min_sal = int(input("Введите минимальную зарплату: "))
    if decide == "да":
        max_sal = int(input("Введите максимальную зарплату: "))
    else:
        max_sal = "-"
    databace_search(min_sal, max_sal, vacancy=vac)
