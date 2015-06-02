# -*- coding: utf-8 -*-
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
        previous_version_link = response.xpath("//p[@id='assentedDate']/a[text()='Previous Versions' or text()='Versions antérieures']/@href").extract()
        html_link = response.xpath("//div[@id='printAll']//a[text()='HTML']/@href").extract()
        xml_link = response.xpath("//div[@id='printAll']//a[text()='XML']/@href").extract()

        response.meta['previous_versions'] = urljoin(response.url, previous_version_link[0]) if len(previous_version_link) > 0 else None
        response.meta['html_link'] = urljoin(response.url, html_link[0]) if len(html_link) > 0 else None

        if len(xml_link) > 0:
            path = urljoin(response.url, xml_link[0])
            yield scrapy.Request(path, self.parse_xml_document, meta=response.meta)

    def parse_xml_document(self, response):
        meta = response.meta

        meta['long_title'] = response.xpath('/Statute/Identification/LongTitle/text()').extract()[0]

        if meta['previous_versions'] is None:
            act_date = response.xpath('/Statute/@startdate').extract()[0]
            loader = ItemLoader(item=ActItem(), response=response)
            loader.add_value('code', response.meta['code'])
            loader.add_value('short_title', response.meta['title'])
            loader.add_value('long_title', response.meta['long_title'])
            loader.add_value('language', response.meta['language'])
            loader.add_value('act_date', act_date)
            loader.add_value('url', response.meta['html_link'])
            yield loader.load_item()
        else:
            yield scrapy.Request(meta['previous_versions'], self.parse_previous_versions, meta=meta)

    @staticmethod
    def parse_previous_versions(response):
        version_links = response.xpath("//div[@id='wb-main-in']/div[@class='wet-boew-texthighlight']/ul//li/a/@href").extract()
        paths = [path for path in version_links]
        for path in paths:
            loader = ItemLoader(item=ActItem(), response=response)
            loader.add_value('code', response.meta['code'])
            loader.add_value('short_title', response.meta['title'])
            loader.add_value('long_title', response.meta['long_title'])
            loader.add_value('language', response.meta['language'])
            loader.add_value('act_date', path[0:8])
            loader.add_value('url', urljoin(response.url, path))
            yield loader.load_item()
