from __future__ import unicode_literals
import pytest
from gitlawca.law_parser import parse_raw_document, reformat_document
from BeautifulSoup import BeautifulSoup

#pylint: disable=W0621
@pytest.fixture(params=['tests/fixtures/C-41.5-eng.html', 'tests/fixtures/C-41.5-fra.html'])
def c41(request):
    with open(request.param) as raw_file:
        text = raw_file.read()
    return parse_raw_document(text)


@pytest.fixture
def c41_text(c41):
    return unicode(c41.prettify(), 'utf8')


@pytest.fixture()
def pretty(c41):
    doc = BeautifulSoup(c41.prettify())
    return reformat_document(doc)


@pytest.fixture()
def pretty_text(pretty):
    return unicode(pretty.prettify(), 'utf8')


def test_raw_files(c41):
    assert 'Version of document' in c41.prettify()[0:200] or 'Version du document' in c41.prettify()[0:200]


def test_parser_removes_version(c41_text, pretty_text):
    assert 'Version of document' in c41_text[0:200] or 'Version du document' in c41_text[0:200]
    assert 'Version of document' not in pretty_text[0:200]
    assert 'Version du document' not in pretty_text[0:200]


def test_parser_deemphasizes_headers(c41, pretty):
    assert len(c41.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != 'Title-of-Act')) > 0
    assert len(pretty.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != 'Title-of-Act')) == 0


def test_parser_removes_marginal_notes(c41, pretty):
    assert len(c41.findAll(lambda tag: tag.name == 'span' and tag.get('class') == 'wb-invisible')) > 0
    assert len(pretty.findAll(lambda tag: tag.name == 'span' and tag.get('class') == 'wb-invisible')) == 0
