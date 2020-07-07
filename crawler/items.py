from scrapy.item import Item, Field


class AuthorItem(Item):
    name = Field()
    url = Field()
    text = Field()
    source = Field()
