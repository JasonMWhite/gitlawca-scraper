from __future__ import unicode_literals
import pytest
from gitlawca.law_parser import parse_raw_document, reformat_document

#pylint: disable=W0621
@pytest.fixture
def c41():
    with open('tests/fixtures/C-41.5.html') as raw_file:
        text = raw_file.read()
    return text

def test_parser(c41):
    output = parse_raw_document(c41)
    assert 'Version of document' in output.prettify()[0:200]

    reformatted = reformat_document(output)
    assert 'Version of document' not in reformatted.prettify()[0:200]
