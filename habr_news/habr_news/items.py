# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HabrNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field() # +
    author_karma = scrapy.Field() # после перехода по ссылке на автора
    author_rating = scrapy.Field() # после перехода по ссылке на автора
    author_specialization = scrapy.Field() # после перехода по ссылке на автора
    comments_counter = scrapy.Field() # +
    hubs = scrapy.Field()
    news_id = scrapy.Field() # после перехода по ссылке на новость
    tags = scrapy.Field()
    text = scrapy.Field() # после перехода по ссылке на новость
    title = scrapy.Field() # +
