import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    link = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    company = scrapy.Field()
    currency = scrapy.Field()
    site = scrapy.Field()
