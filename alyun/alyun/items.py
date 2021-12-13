# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Id = scrapy.Field()
    link_first = scrapy.Field()
    link_next = scrapy.Field()
    title = scrapy.Field()
    del_url = scrapy.Field()
    context = scrapy.Field()
    yun_href = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    response_url = scrapy.Field()

