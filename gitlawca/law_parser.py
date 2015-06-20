from __future__ import unicode_literals
from html2text import html2text
from BeautifulSoup import BeautifulSoup


def parse_raw_document(data):
    doc = BeautifulSoup(data)
    output = doc.find(lambda tag: tag.get('id') == 'wb-cont')
    output = unicode(output.prettify(), 'utf8')
    return output


def prettify_to_markdown(data):
    return html2text(data)
