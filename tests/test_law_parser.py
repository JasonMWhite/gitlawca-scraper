from __future__ import unicode_literals
import pytest
from gitlawca.law_parser import parse_raw_document, reformat_document, reformatted_to_markdown
from bs4 import BeautifulSoup

#pylint: disable=W0621
@pytest.fixture(params=['tests/fixtures/C-41.5-eng.html', 'tests/fixtures/C-41.5-fra.html'])
def c41(request):
    with open(request.param) as raw_file:
        text = raw_file.read()
    return parse_raw_document(text)


@pytest.fixture
def c41_text(c41):
    return unicode(str(c41), 'utf8')


@pytest.fixture()
def pretty(c41):
    doc = BeautifulSoup(str(c41))
    doc = reformat_document(doc)
    return doc


@pytest.fixture()
def pretty_text(pretty):
    return unicode(str(pretty), 'utf8')


@pytest.fixture()
def markdown(pretty):
    return reformatted_to_markdown(pretty)


def test_raw_files(c41):
    assert 'Version of document' in c41.prettify()[0:200] or 'Version du document' in c41.prettify()[0:200]


def test_parser_removes_version(c41_text, pretty_text):
    assert 'Version of document' in c41_text[0:200] or 'Version du document' in c41_text[0:200]
    assert 'Version of document' not in pretty_text[0:200]
    assert 'Version du document' not in pretty_text[0:200]


def test_parser_deemphasizes_headers(c41, pretty):
    assert len(c41.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != ['Title-of-Act'])) > 0
    assert len(pretty.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != ['Title-of-Act'])) == 0


def test_parser_removes_marginal_notes(c41, pretty):
    assert len(c41.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible'])) > 0
    assert len(pretty.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible'])) == 0


def test_parser_bolds_numbers_properly(c41, pretty, markdown):
    assert len(c41.findAll(lambda tag: tag.get('class') == ['sectionLabel'] and tag.parent.parent.name == 'strong')) > 0
    assert pretty.find(lambda tag: tag.get('class') == ['sectionLabel'] and tag.parent.parent.name == 'strong') is None
    assert '**1.**' in markdown
