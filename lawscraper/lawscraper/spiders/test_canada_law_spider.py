from __future__ import unicode_literals
from lawscraper.lawscraper.spiders.canada_law import CanadaLawSpider
from scrapy.http.response.xml import XmlResponse
from scrapy.http.response.html import HtmlResponse
import pytest
from mock import Mock

#pylint: disable=R0201
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
        assert response.callback == spider.parse_toc

    @pytest.fixture
    def toc_response_with_previous_version(self):
        body = "<header><h1 id='wb-cont' class='HeadTitle'>Access to Information Act</h1>" + \
               "<div id='printAll'><p id='FullDoc'>Full Document</p><ul><li><a href='FullText.html'>HTML</a></li>" \
               "<li><a href='/eng/XML/A-1.xml'>XML</a><span class='fileSize'>[240 KB]</span></li>" \
               "<li><a href='/PDF/A-1.pdf'>PDF</a><span class='fileSize'>[341 KB]</span></li></ul></div>" \
               "<div class='info'><p id='assentedDate'>Act current to 2015-05-11 and last amended on 2015-04-23. " \
               "<a href='PITIndex.html'>Previous Versions</a></p></div>" \
               "<div class='tocNotes'>Notes :<ul><li>See coming into force provision and notes, where applicable.</li>" \
               "<li>Shaded provisions are not in force. " \
               "<a href='/eng/FAQ/#g10'>Help</a></li></ul></div><div class='lineSeparator goldLineTop'></div>" \
               "</header>"
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/index.html'), body=str(body), request=request)

    def test_parse_toc_with_previous_version(self, spider, toc_response_with_previous_version):
        response = [x for x in spider.parse_toc(toc_response_with_previous_version)]
        assert len(response) == 1
        response = response[0]
        assert response.meta['code'] == 'A-1'
        assert response.meta['language'] == 'eng'
        assert response.meta['title'] == 'Access to Information Act'
        assert response.meta['html_link'] == 'http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html'
        assert response.meta['previous_versions'] == 'http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html'
        assert response.url == str('http://laws-lois.justice.gc.ca/eng/XML/A-1.xml')
        assert response.callback == spider.parse_xml_document

    @pytest.fixture
    def toc_response_without_previous_version(self):
        body = "<header><h1 id='wb-cont' class='HeadTitle'>Access to Information Act</h1>" + \
               "<div id='printAll'><p id='FullDoc'>Full Document</p><ul><li><a href='FullText.html'>HTML</a></li>" \
               "<li><a href='/eng/XML/A-1.xml'>XML</a><span class='fileSize'>[240 KB]</span></li>" \
               "<li><a href='/PDF/A-1.pdf'>PDF</a><span class='fileSize'>[341 KB]</span></li></ul></div>" \
               "<div class='tocNotes'>Notes :<ul><li>See coming into force provision and notes, where applicable.</li>" \
               "<li>Shaded provisions are not in force. " \
               "<a href='/eng/FAQ/#g10'>Help</a></li></ul></div><div class='lineSeparator goldLineTop'></div>" \
               "</header>"
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/index.html'), body=str(body), request=request)

    def test_parse_toc_without_previous_version(self, spider, toc_response_without_previous_version):
        response = [x for x in spider.parse_toc(toc_response_without_previous_version)]
        assert len(response) == 1
        response = response[0]
        assert response.meta['code'] == 'A-1'
        assert response.meta['language'] == 'eng'
        assert response.meta['title'] == 'Access to Information Act'
        assert response.meta['html_link'] == 'http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html'
        assert response.meta['previous_versions'] is None
        assert response.url == str('http://laws-lois.justice.gc.ca/eng/XML/A-1.xml')
        assert response.callback == spider.parse_xml_document

    @pytest.fixture
    def toc_response_without_required_data(self):
        body = "<div id='wb-main-in'><header>Something</header></div>"
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/index.html'), body=str(body), request=request)

    def test_parse_toc_without_required_data(self, spider, toc_response_without_required_data):
        response = [x for x in spider.parse_toc(toc_response_without_required_data)]
        assert len(response) == 0

    @pytest.fixture
    def previous_versions_response(self):
        body = "<div id='wb-main' role='main'><div id='wb-main-in'><div class='wet-boew-texthighlight'>" + \
               "<h2 id='wb-cont' class='PITIndex'>Full Documents available for previous versions</h2>" + \
               "<ul><li>2015<ul><li><a href='20150423/P1TT3xt3.html'>From 2015-04-23 to 2015-05-11</a></li>" + \
               "<li><a href='20150226/P1TT3xt3.html'>From 2015-02-26 to 2015-04-22</a></li>" + \
               "<li><a href='20150207/P1TT3xt3.html'>From 2015-02-07 to 2015-02-25</a></li>" + \
               "</ul></li></ul></div></div></div>"
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act',
            'long_title': 'Long Access to Information Act Title'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html'), body=str(body), request=request)

    def test_parse_previous_versions(self, spider, previous_versions_response):
        items = [x for x in spider.parse_previous_versions(previous_versions_response)]
        assert len(items) == 3
        for item in items:
            assert item['code'] == ['A-1']
            assert item['short_title'] == ['Access to Information Act']
            assert item['long_title'] == ['Long Access to Information Act Title']
            assert item['language'] == ['eng']

        assert items[0]['url'] == [str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150423/P1TT3xt3.html')]
        assert items[0]['act_date'] == ['20150423']
        assert items[1]['url'] == [str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150226/P1TT3xt3.html')]
        assert items[1]['act_date'] == ['20150226']
        assert items[2]['url'] == [str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150207/P1TT3xt3.html')]
        assert items[2]['act_date'] == ['20150207']

    @pytest.fixture
    def xml_document(self):
        body = '<Statute bill-origin="commons" bill-type="govt-public" xml:lang="en" in-force="yes" startdate="20150423">' \
               '<Identification><LongTitle>A long title</LongTitle></Identification>' \
               '</Statute>'
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act',
            'html_link': 'http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html',
            'previous_versions': None
        }
        request = Mock()
        request.meta = meta
        return XmlResponse(str('http://laws-lois.justice.gc.ca/eng/XML/A-1.xml'), body=str(body), request=request)

    def test_parse_xml_document_with_previous_versions(self, spider, xml_document):
        xml_document.meta['previous_versions'] = 'http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html'
        response = [x for x in spider.parse_xml_document(xml_document)]
        assert len(response) == 1
        response = response[0]
        assert response.meta['code'] == 'A-1'
        assert response.meta['language'] == 'eng'
        assert response.meta['title'] == 'Access to Information Act'
        assert response.meta['long_title'] == 'A long title'
        assert response.meta['html_link'] == 'http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html'
        assert response.url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html')
        assert response.callback == spider.parse_previous_versions

    def test_parse_xml_document_without_previous_versions(self, spider, xml_document):
        response = [x for x in spider.parse_xml_document(xml_document)]
        assert len(response) == 1
        response = response[0]
        assert response['code'] == ['A-1']
        assert response['short_title'] == ['Access to Information Act']
        assert response['long_title'] == ['A long title']
        assert response['act_date'] == ['20150423']
        assert response['url'] == ['http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html']
        assert response['language'] == ['eng']
