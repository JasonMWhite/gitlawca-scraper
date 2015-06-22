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
    assert len(pretty.findAll(lambda tag: tag.name == 'h1' and tag.get('class') == ['Title-of-Act'])) == 1
    assert len(pretty.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != ['Title-of-Act'])) == 0


def test_parser_removes_marginal_notes(c41, pretty):
    assert len(c41.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible'])) > 0
    assert len(pretty.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible'])) == 0


def test_parser_removes_provision_lists(c41, pretty):
    provision_list = c41.ul
    assert provision_list is not None
    assert '2.' == provision_list.text[0:2]

    list_entry = pretty.find(lambda tag: tag.name == 'p' and tag.get('class') == ['Subsection'])
    assert list_entry is not None
    assert '2.' == list_entry.text[0:2]
    assert pretty.find('ul').get('class') == ['ProvisionList']

    with open('test.html', 'w') as f:
        f.write(str(pretty))


def test_parser_reformats_definitions(c41, pretty):
    definitions = c41.find(lambda tag: tag.name == 'dl' and tag.get('class') == ['Definition'])
    first_definition = definitions.dt
    assert len(first_definition.find_all(lambda tag: tag.name == 'p' and tag.get('class') == ['MarginalNoteDefinedTerm'])) == 2

    pretty_definitions = pretty.find(lambda tag: tag.name == 'dl' and tag.get('class') == ['Definition'])
    first_pretty_definition = pretty_definitions.dt
    assert len(first_pretty_definition.find_all('p')) == 1


def test_parser_reformats_links(c41, pretty):
    link = c41.find(lambda tag: tag.name == 'a' and tag.get('href') is not None)
    assert link.get('href') == '/eng/acts/C-41.5' or link.get('href') == '/fra/lois/C-41.5'

    pretty_link = pretty.find(lambda tag: tag.name == 'a' and tag.get('href') is not None)
    assert pretty_link['href'] == '/canada/eng/acts/C/C-41.5.md' or pretty_link['href'] == '/canada/fra/lois/C/C-41.5.md'


def test_parser_reformats_multipart_headers(c41, pretty):
    header1 = c41.find(lambda tag: tag.name == 'h1' and tag.get('id') == 'h-3')
    assert len(header1.find_all('span')) == 2
    header2 = c41.find(lambda tag: tag.name == 'h1' and tag.get('id') == 'h-6')
    assert len(header2.find_all('span')) == 3

    pretty_header1 = pretty.find(lambda tag: tag.name == 'h2' and tag.get('id') == 'h-3')
    assert len(pretty_header1.find_all('span')) == 1
    pretty_header2 = pretty.find(lambda tag: tag.name == 'h2' and tag.get('id') == 'h-6')
    assert len(pretty_header2.find_all('span')) == 1


def test_parser_fixes_asterisks(c41, pretty):
    assert len(c41.find_all(lambda tag: tag.name == 'sup' and tag.text == '*')) > 0
    assert len(pretty.find_all(lambda tag: tag.name == 'sup' and tag.text == '*')) == 0
    assert len(pretty.find_all(lambda tag: tag.name == 'sup' and tag.text == '(*)')) > 0
