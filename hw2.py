import json
import requests
from bs4 import BeautifulSoup as bs


def price_processing(p):
    p = p.replace(" ", "")
    currency = ""
    while not p[-1].isdigit():
        currency = p[-1] + currency
        p = p[:-1]
    if p[0] == "о":
        min_price = p[2:]
        max_price = "-"
    elif p[0] == "д":
        max_price = p[2:]
        min_price = "-"
    else:
        p = p.split("–")
        min_price = p[0]
        max_price = p[1]
    result = {
        "min_price": min_price,
        "max_price": max_price,
        "currency": currency
    }
    return result


def save_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        print(f"Json file saved: {file}")


def get(url_, headers_, params_):
    result = requests.get(url_, headers=headers_, params=params_)
    return result


vacancy = input("Введите вакансию: ")
vacancy_num = int(input("Введите количество обрабатываемых страниц: "))
vacancy_salary = input("Зарплата указана? (да/нет) ").lower()
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

        price = item.find(attrs={"class": "vacancy-serp-item__sidebar"}).text.replace("\u202f", " ")
        price = price_processing(price)
        info["currency"] = price["currency"]
        info["min_price"] = price["min_price"]
        info["max_price"] = price["max_price"]
        info["get_from"] = my_request.url
        items_info.append(info)

    if page < (vacancy_num - 1):
        page += 1
        params["page"] = page
    else:
        break

save_json({vacancy: items_info}, 'saved_vacancy_json')

print("Done!")
