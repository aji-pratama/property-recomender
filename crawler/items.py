from scrapy.item import Item, Field


class PropertyItem(Item):
    name = Field()
    url = Field()
    text = Field()
    source = Field()
