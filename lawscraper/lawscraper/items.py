from __future__ import unicode_literals
from scrapy import Item, Field


class ActItem(Item):
    code = Field()
    short_title = Field()
    long_title = Field()
    act_date = Field()
    body = Field()
    language = Field()
