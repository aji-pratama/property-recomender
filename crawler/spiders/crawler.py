import scrapy

from crawler.items import PropertyItem
from crawler.utils import clean_html


class DotPropertySpider(scrapy.Spider):
    name = 'dotproperty'
    start_urls = ['https://www.dotproperty.id/properties-for-sale/search/jabodetabek']

    def parse(self, response):
        author_page_links = response.css('.left-block a')
        yield from response.follow_all(author_page_links, self.parse_property)

        pagination_links = response.css('ul.pagination li a[rel="next"]::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_property(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = PropertyItem()
        item = {
            'name': extract_with_css('h1.page-title a::text'),
            'url': response.url,
            'text': clean_html(extract_with_css('.text-description')),
            'source': 'Dotproperty.id'
        }
        yield item


class RumahComSpider(scrapy.Spider):
    name = 'rumahcom'
    allowed_domains = ['www.rumah.com']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    # start_urls = ['https://www.rumah.com/properti-dijual?freetext=jabodetabek&market=residential&ps=1']
    start_urls = ['https://www.rumah.com/properti-dijual?freetext=jabodetabek&market=residential&ps=1']
    # handle_httpstatus_list = [403]

    # def start_requests(self):
    #     headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    #     for url in self.start_urls:
    #         yield Request(url, headers=headers)

    def parse(self, response):
        author_page_links = response.css('.ellipsis.text-transform-none a')
        yield from response.follow_all(author_page_links, self.parse_property)

        pagination_links = response.css('li.pagination-next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_property(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_description(text):
            return clean_html(extract_with_css(text).replace('Baca Selengkapnya', '').replace('Deskripsi', ''))

        item = PropertyItem()
        item = {
            'name': extract_with_css('h1.text-transform-none::text'),
            'url': response.url,
            'text': extract_description('.listing-details-text'),
            'source': 'Rumah.com'
        }
        yield item


class LamudiSpider(scrapy.Spider):
    name = 'lamudi'
    start_urls = ['https://www.lamudi.co.id/buy/?q=jabodetabek']

    def parse(self, response):
        author_page_links = response.css('.js-listing-link')
        yield from response.follow_all(author_page_links, self.parse_property)

        pagination_links = response.css('.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_property(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item = PropertyItem()
        item = {
            'name': extract_with_css('.Header-title-block h1::text'),
            'url': response.url,
            'text': clean_html(extract_with_css('.ViewMore-text-description')),
            'source': 'Lamudi.co.id'
        }
        yield item
