from __future__ import unicode_literals
from html2text import html2text
from BeautifulSoup import BeautifulSoup


def parse_raw_document(data):
    doc = BeautifulSoup(data)
    output = doc.find(lambda tag: tag.get('id') == 'wb-cont')
    return output


def strip_versioning(doc):
    versioning = doc.find(lambda tag: tag.get('class') == 'info')
    if versioning is not None and 'Version of document' in versioning.text:
        versioning.decompose()
    return doc


def reformat_document(doc):
    return strip_versioning(doc)


def prettify_to_markdown(doc):
    doc = reformat_document(doc)
    doc = unicode(doc.prettify(), 'utf8')
    return html2text(doc)
