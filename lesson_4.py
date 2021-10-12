"""
1. Написать приложение, которое собирает основные новости с сайтов
https://news.mail.ru,
https://lenta.ru,
https://yandex.ru/news.
Для парсинга использовать XPath. Структура данных должна содержать:
 название источника;
 наименование новости;
 ссылку на новость;
 дата публикации.
2. Сложить собранные данные в БД
"""

import requests
import time
from datetime import datetime
from pymongo import MongoClient
from lxml import html

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.96 Safari/537.36"
}

MONGO_URL = "127.0.0.1:27017"
MONGO_DB = "News"
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]


def update_db(col, inf):
    col_name = col
    col = db[col]
    for item in inf:
        col.update_one({"$and": [{'news_name': {"$eq": item['news_name']}}, {'source': {"$eq": item['source']}}]},
                       {'$set': item}, upsert=True)
    print(f'----- {MONGO_DB} databace updating completed! Collection name: {col_name} -----\n')


def get_news_lenta():
    url = "https://lenta.ru/"
    r = requests.get(url, headers)
    dom = html.fromstring(r.text)
    item_xpath = '//section[@class="row b-top7-for-main js-top-seven"]//div[contains(@class, "item")]'
    items = dom.xpath(item_xpath)
    info = list()
    for item in items:
        info_item = dict()
        xpath_item_name = ".//a/text()"

        info_item["source"] = "Lenta.ru"
        info_item["news_name"] = item.xpath(xpath_item_name)[0].replace('\xa0', '')
        info_item["news_url"] = url + item.xpath(".//a/@href")[0]
        info_item["news_datetime"] = item.xpath(".//a/time/@datetime")[0]
        info.append(info_item)
        time.sleep(0.01)
    update_db("Lenta.ru", info)
    return info


def get_news_yandex():
    url = "https://yandex.ru/news"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    info_list = list()
    xpath_for_item = '//div[contains(@class, "news-top-flexible-stories")]/div'
    items = dom.xpath(xpath_for_item)
    for item in items:
        info = dict()
        xpath_item_name = ".//h2/text()"
        info["source"] = item.xpath('.//span[contains(@class, "__source")]//a/text()')[0]
        info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
        info["news_url"] = item.xpath(".//a/@href")[0]
        info["news_datetime"] = datetime.fromtimestamp(int(item.xpath('.//a/@data-log-id')[0].split('-')[1][:-3]))
        info_list.append(info)
        time.sleep(0.01)
    update_db("Yandex.ru", info_list)
    return info_list


def get_news_mail():
    url = "https://news.mail.ru"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    item_xpath = '//div[@class="wrapper"]//div[@data-module="TrackBlocks"]//div[contains(@class, "__item")]'
    items = dom.xpath(item_xpath)
    info_list = list()
    for item in items:
        info = dict()
        xpath_item_name = ".//span[contains(@class, '__title')]/text()"
        info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
        info["news_url"] = item.xpath(".//a/@href")[0]
        info["source"] = get_mail_info(item.xpath(".//a/@href")[0])[0]
        info["news_datetime"] = get_mail_info(item.xpath(".//a/@href")[0])[1]
        info_list.append(info)
    item_xpath = '//ul[contains(@data-module, "TrackBlocks")]//li[@class="list__item"]'
    items = dom.xpath(item_xpath)
    for item in items:
        info = dict()
        xpath_item_name = ".//a/text()"
        info["news_name"] = item.xpath(xpath_item_name)[0].replace(u'\xa0', u' ')
        info["news_url"] = item.xpath(".//a/@href")[0]
        info["source"] = get_mail_info(item.xpath(".//a/@href")[0])[0]
        info["news_datetime"] = get_mail_info(item.xpath(".//a/@href")[0])[1]
        info_list.append(info)
        time.sleep(0.01)
    update_db("Mail.ru", info_list)
    return info_list


def get_mail_info(url):
    r = requests.get(url, headers=headers)
    xpath_for_item = '//div[@class="breadcrumbs breadcrumbs_article js-ago-wrapper"]'
    dom = html.fromstring(r.text)
    items = dom.xpath(xpath_for_item)
    for item in items:
        source = item.xpath(".//a/span/text()")[0]
        news_datetime = item.xpath('.//span//@datetime')[0]
    return [source, news_datetime]


get_news_yandex()
get_news_mail()
get_news_lenta()
