from __future__ import unicode_literals
from lawscraper.lawscraper.spiders.canada_law import CanadaLawSpider
from scrapy.http.response.xml import XmlResponse
import pytest


class TestCanadaLawSpider(object):

    @pytest.fixture
    def spider(self):
        return CanadaLawSpider()

    @pytest.fixture
    def acts_response(self):
        body = "<ActsRegsList><Acts><Act>" + \
            "<UniqueId>A-1</UniqueId>" + \
            "<Language>eng</Language>" + \
            "<Title>Bill Test</Title>" + \
            "<LinkToHTMLToC>http://laws.justice.gc.ca/A-1.html</LinkToHTMLToc>" + \
            "</Act></Acts></ActsRegsList>"
        return XmlResponse(str('laws-lois.justice.gc.ca'), body=str(body))

    def test_parse(self, spider, acts_response):
        response = [x for x in spider.parse(acts_response)]
        assert len(response) == 1
        response = response[0]
        assert response.meta['code'] == str('A-1')
        assert response.meta['language'] == str('eng')
        assert response.meta['title'] == str('Bill Test')
        assert response.url == str('http://laws.justice.gc.ca/A-1.html')
        assert response.callback == spider.parse_act

    def test_parse_act(self):
        assert True

    def test_parse_previous_versions(self):
        assert True

    def test_parse_xml_document(self):
        assert True

    def test_parse_full_document(self):
        assert True
