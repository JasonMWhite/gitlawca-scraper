from __future__ import unicode_literals
from lawscraper.lawscraper.spiders.canada_law import CanadaLawSpider
from scrapy.http.response.xml import XmlResponse
from scrapy.http.response.html import HtmlResponse
import pytest
from mock import Mock


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
        assert response.url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html')
        assert response.callback == spider.parse_previous_versions

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
            'title': 'Access to Information Act'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/PITIndex.html'), body=str(body), request=request)

    def test_parse_previous_versions(self, spider, previous_versions_response):
        responses = [x for x in spider.parse_previous_versions(previous_versions_response)]
        assert len(responses) == 3
        for response in responses:
            assert response.meta['code'] == 'A-1'
            assert response.meta['language'] == 'eng'
            assert response.meta['title'] == 'Access to Information Act'
            assert response.callback == spider.parse_full_document

        assert responses[0].url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150423/P1TT3xt3.html')
        assert responses[1].url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150226/P1TT3xt3.html')
        assert responses[2].url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150207/P1TT3xt3.html')

    @pytest.fixture
    def xml_document(self):
        body = '<Statute bill-origin="commons" bill-type="govt-public" xml:lang="en" in-force="yes" startdate="20150423"></Statute>'
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act',
            'html_link': 'http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html'
        }
        request = Mock()
        request.meta = meta
        return XmlResponse(str('http://laws-lois.justice.gc.ca/eng/XML/A-1.xml'), body=str(body), request=request)

    def test_parse_xml_document(self, spider, xml_document):
        response = [x for x in spider.parse_xml_document(xml_document)]
        assert len(response) == 1
        response = response[0]
        assert response.meta['code'] == 'A-1'
        assert response.meta['language'] == 'eng'
        assert response.meta['title'] == 'Access to Information Act'
        assert response.meta['act_date'] == '20150423'
        assert 'html_link' not in response.meta
        assert response.url == str('http://laws-lois.justice.gc.ca/eng/acts/A-1/FullText.html')
        assert response.callback == spider.parse_full_document
        assert True

    @pytest.fixture
    def full_document(self):
        body = '<div id="wb-main-in">' + \
               '<div class="archiveBar"><a href="/eng/ArchiveNote">This Web page has been archived on the Web.</a></div>' + \
               '<div id="wb-cont" class="docContents">' + \
               '<section><div class="wet-boew-texthighlight">' + \
               '<div class="info">Version of document from 2015-04-23 to 2015-05-11:</div>' + \
               '<section class="intro"><header><h1 class="Title-of-Act">Access to Information Act</h1>' \
               '<p class="ChapterNumber"><abbr title="Revised Statutes of Canada">R.S.C.</abbr>, 1985, c. A-1</p></header>' \
               '<p class="LongTitle" id="id-lt">An Act to extend the present laws of Canada that provide access to information under the control of the Government of Canada</p>' \
               '</section></div></section></div></div></div>'
        meta = {
            'code': 'A-1',
            'language': 'eng',
            'title': 'Access to Information Act',
            'act_date': '20150423'
        }
        request = Mock()
        request.meta = meta
        return HtmlResponse(str('http://laws-lois.justice.gc.ca/eng/acts/A-1/20150423/P1TT3xt3.html'), body=str(body), request=request)

    def test_parse_full_document_with_date(self, spider, full_document):
        items = [x for x in spider.parse_full_document(full_document)]
        assert len(items) == 1
        item = items[0]
        assert item['code'] == ['A-1']
        assert item['short_title'] == ['Access to Information Act']
        assert item['language'] == ['eng']
        assert item['long_title'] == ['An Act to extend the present laws of Canada that provide access to information under the control of the Government of Canada']
        assert item['act_date'] == ['20150423']
        assert len(item['body'][0]) == 478

    def test_parse_full_document_without_date(self, spider, full_document):
        del full_document.request.meta['act_date']
        items = [x for x in spider.parse_full_document(full_document)]
        assert len(items) == 1
        item = items[0]
        assert item['code'] == ['A-1']
        assert item['short_title'] == ['Access to Information Act']
        assert item['language'] == ['eng']
        assert item['long_title'] == ['An Act to extend the present laws of Canada that provide access to information under the control of the Government of Canada']
        assert item['act_date'] == ['20150423']
        assert len(item['body'][0]) == 478
