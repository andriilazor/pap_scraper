# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PapItem(scrapy.Item):
    """Item representing a news article extracted from pap.pl."""
    title = scrapy.Field()
    url = scrapy.Field()
