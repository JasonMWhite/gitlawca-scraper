from __future__ import unicode_literals
from html2text import html2text
from bs4 import BeautifulSoup


def parse_raw_document(data):
    doc = BeautifulSoup(data)
    output = doc.find(lambda tag: tag.get('id') == 'wb-cont')
    return output


def strip_versioning(doc):
    versioning = doc.find(lambda tag: tag.get('class') == ['info'])
    if versioning is not None and ('document' in versioning.text):
        versioning.decompose()
    return doc


def deemphasize_headers(doc):
    headers = doc.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != 'Title-of-Act')
    for header in headers:
        header.name = 'h2'
    return doc


def remove_marginal_notes(doc):
    for tag in doc.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible']):
        tag.decompose()
    return doc


def fix_bold_numbering(doc):
    for tag in doc(lambda tag: tag.get('class') == ['sectionLabel'] and tag.parent.parent.name == 'strong'):
        strong_tag = tag.parent.parent
        number = tag.text.strip()
        new_strong_tag = doc.new_tag('strong')
        new_strong_tag.string = number
        strong_tag.replaceWith(new_strong_tag)
    return doc


rules = [
    strip_versioning,
    deemphasize_headers,
    remove_marginal_notes,
    fix_bold_numbering
]


def reformat_document(doc):
    for rule in rules:
        doc = rule(doc)
    return doc


def reformatted_to_markdown(doc):
    return html2text(unicode(str(doc), 'utf8'))


def prepare_markdown(doc):
    doc = parse_raw_document(doc)
    doc = reformat_document(doc)
    doc = reformatted_to_markdown(doc)
    return doc
