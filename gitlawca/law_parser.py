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
    headers = doc.findAll(lambda tag: tag.name == 'h1' and tag.get('class') != ['Title-of-Act'])
    for header in headers:
        header.name = 'h2'
    return doc


def remove_marginal_notes(doc):
    for tag in doc.findAll(lambda tag: tag.name == 'span' and tag.get('class') == ['wb-invisible']):
        tag.decompose()
    return doc

def remove_provision_lists(doc):
    main_node = doc.find(lambda tag: tag.name == 'div' and tag.get('class') == ['wet-boew-texthighlight'])
    if main_node is None:
        return doc

    def parse_provision_lists(main_node):
        for content_node in [x for x in main_node.children]:
            if content_node.name != 'ul':
                yield content_node.extract()
            else:
                for list_entry in [x for x in content_node.children]:
                    if list_entry.name == 'li':
                        for list_child in [x for x in list_entry.children]:
                            yield list_child.extract()

    new_doc = BeautifulSoup()
    for tag in parse_provision_lists(main_node):
        new_doc.append(tag)

    return new_doc


def reformat_definitions(doc):
    definitions = doc.find(lambda tag: tag.name == 'dl' and tag.get('class') == ['Definition'])
    if definitions is None:
        return doc

    def extract_term_nodes():
        for child in definitions.children:
            if child.name == 'dt':
                yield child

    for term_node in extract_term_nodes():
        terms = []
        for para in term_node.children:
            if para.span is None:
                continue
            if para.span.get('class') == ['DefinedTerm']:
                terms.append('**{}**'.format(para.span.text))
            elif para.span.get('class') == ['DefinedTermLink']:
                terms.append('_{}_'.format(para.span.text))

        term_node.clear()
        if len(terms) > 0:
            new_defn = doc.new_tag('p')
            new_defn.string = ' - '.join(terms)
            term_node.append(new_defn)
    return doc


rules = [
    strip_versioning,
    deemphasize_headers,
    remove_marginal_notes,
    remove_provision_lists,
    reformat_definitions
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
