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


def repoint_links(doc):
    for link in doc.find_all(lambda tag: tag.name == 'a' and tag.get('href', '').startswith('/')):
        link_parts = link['href'].split('/')[1:]
        if len(link_parts) < 3:
            continue

        link_parts.insert(0, 'canada')
        link_parts.insert(3, link_parts[3].split('-')[0])
        link_parts[-1] = '{}.md'.format(link_parts[-1])

        link['href'] = '/' + '/'.join(link_parts)
    return doc


def fix_multipart_headers(doc):
    for header in doc.find_all('h2'):
        spans = []
        for header_child in [x for x in header.children]:
            if header_child.name == 'span':
                spans.append(header_child.extract())

        if len(spans) > 0:
            header_text = [span.text for span in spans]
            new_header = doc.new_tag('span')
            new_header.string = ' - '.join(header_text)
            header.append(new_header)
    return doc


def fix_asterisks(doc):
    for sup in doc.find_all(lambda tag: tag.name == 'sup' and tag.text == '*'):
        sup.string = '(*)'
    return doc


rules = [
    strip_versioning,
    deemphasize_headers,
    remove_marginal_notes,
    remove_provision_lists,
    reformat_definitions,
    repoint_links,
    fix_multipart_headers,
    fix_asterisks
]


def reformat_document(doc):
    for rule in rules:
        doc = rule(doc)
    return doc


def reformatted_to_markdown(doc):
    return html2text(unicode(str(doc), 'utf8'), bodywidth=0)


def prepare_markdown(doc):
    doc = parse_raw_document(doc)
    doc = reformat_document(doc)
    doc = reformatted_to_markdown(doc)
    return doc
