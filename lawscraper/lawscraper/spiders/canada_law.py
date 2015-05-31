from __future__ import unicode_literals
import scrapy
from urlparse import urljoin
from lawscraper.lawscraper.items import ActItem
from scrapy.contrib.loader import ItemLoader


class CanadaLawSpider(scrapy.Spider):
    name = "canada-law"
    allowed_domains = ["laws-lois.justice.gc.ca"]
    start_urls = (
        'http://laws-lois.justice.gc.ca/eng/XML/Legis.xml',
    )

    def parse(self, response):
        acts = response.xpath("//Acts/Act")
        for act in acts:
            code = act.xpath("UniqueId/text()").extract()[0]
            language = act.xpath("Language/text()").extract()[0]
            title = act.xpath("Title/text()").extract()[0]
            path = act.xpath("LinkToHTMLToC/text()").extract()[0]
            yield scrapy.Request(path, self.parse_toc, meta={'code': code, 'language': language, 'title': title})

    def parse_toc(self, response):
        previous_version_links = response.xpath("//p[@id='assentedDate']/a[text()='Previous Versions']/@href").extract()
        if len(previous_version_links) > 0:
            path = urljoin(response.url, previous_version_links[0])
            yield scrapy.Request(path, self.parse_previous_versions, meta=response.meta)
        else:
            html_link = response.xpath("//div[@id='printAll']//a[text()='HTML']/@href").extract()
            if len(html_link) > 0:
                html_link = html_link[0]
                xml_link = response.xpath("//div[@id='printAll']//a[text()='XML']/@href").extract()[0]
                meta = response.meta
                meta['html_link'] = urljoin(response.url, html_link)
                path = urljoin(response.url, xml_link)
                yield scrapy.Request(path, self.parse_xml_document, meta=meta)

    def parse_previous_versions(self, response):
        version_links = response.xpath("//div[@id='wb-main-in']/div[@class='wet-boew-texthighlight']/ul//li/a/@href").extract()
        paths = [urljoin(response.url, path) for path in version_links]
        for path in paths:
            yield scrapy.Request(path, self.parse_full_document, meta=response.meta)

    def parse_xml_document(self, response):
        meta = response.meta
        html_link = meta.pop('html_link')

        act_date = response.xpath('/Statute/@startdate').extract()[0]
        meta['act_date'] = act_date
        yield scrapy.Request(html_link, self.parse_full_document, meta=meta)

    def parse_full_document(self, response):
        content = response.xpath("//div[@id='wb-main-in']//div[@class='wet-boew-texthighlight']")

        loader = ItemLoader(item=ActItem(), selector=content, response=response)
        loader.add_value('code', response.meta['code'])
        loader.add_value('short_title', response.meta['title'])
        loader.add_value('language', response.meta['language'])
        loader.add_xpath('long_title', ".//p[@id='id-lt']/text()")
        loader.add_xpath('body', '.')
        if 'act_date' in response.meta:
            loader.add_value('act_date', response.meta['act_date'])
        else:
            act_date = content.xpath("div[@class='info']/text()").extract()[0]
            act_date = act_date[-25:-15].replace('-', '')
            loader.add_value('act_date', act_date)

        yield loader.load_item()
