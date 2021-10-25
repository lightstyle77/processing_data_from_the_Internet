from itemloaders.processors import TakeFirst
import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    follow_list = scrapy.Field(output_processor=TakeFirst())
    fol_username = scrapy.Field(output_processor=TakeFirst())
    fol_user_id = scrapy.Field(output_processor=TakeFirst())
    pic_url = scrapy.Field(output_processor=TakeFirst())
    j_body = scrapy.Field(output_processor=TakeFirst())
    username = scrapy.Field(output_processor=TakeFirst())
    user_id = scrapy.Field(output_processor=TakeFirst())
