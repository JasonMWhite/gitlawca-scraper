from __future__ import unicode_literals
from html2text import html2text
from BeautifulSoup import BeautifulSoup


def parse_raw_document(data):
    doc = BeautifulSoup(data)
    output = doc.find(lambda tag: tag.get('id') == 'wb-cont')
    return output


def strip_versioning(doc):
    versioning = doc.find(lambda tag: tag.get('class') == 'info')
    if versioning is not None and ('document' in versioning.text):
        versioning.decompose()
    return doc


def deemphasize_headers(doc):
    headers = doc.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != 'Title-of-Act')
    for header in headers:
        header.name = 'h2'
    return doc


def remove_marginal_notes(doc):
    for tag in doc.findAll(lambda tag: tag.name == 'span' and tag.get('class') == 'wb-invisible'):
        tag.decompose()
    return doc


rules = [
    strip_versioning,
    deemphasize_headers,
    remove_marginal_notes
]


def reformat_document(doc):
    for rule in rules:
        doc = rule(doc)
    return doc


def prettify_to_markdown(doc):
    doc = reformat_document(doc)
    doc = unicode(doc.prettify(), 'utf8')
    return html2text(doc)