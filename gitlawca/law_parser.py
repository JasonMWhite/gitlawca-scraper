from __future__ import unicode_literals
from html2text import html2text
from bs4 import BeautifulSoup


def parse_raw_document(data):
    doc = BeautifulSoup(data)
    content_node = doc.find(lambda tag: tag.get('id') == 'wb-cont')
    new_doc = BeautifulSoup()
    new_doc.append(content_node.extract())
    return new_doc


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
    def is_subsection(tag):
        return tag.name == 'p' and tag.get('class') == ['Subsection']

    def appropriate_provision(tag):
        return tag.name == 'ul' and tag.get('class') == ['ProvisionList'] and tag.find_previous_sibling(is_subsection) is None and tag.find_parent(lambda parent: parent.name == 'ul' and parent.get('class') == ['ProvisionList'] and parent.find_previous_sibling(is_subsection) is None) is None

    for provision_list in [x for x in doc.find_all(appropriate_provision)]:
        nodes_to_insert = []
        for list_entry in [x for x in provision_list.children]:
            if list_entry.name == 'li':
                for list_element in [x for x in list_entry.children]:
                    nodes_to_insert.append(list_element.extract())
            else:
                nodes_to_insert.append(list_entry.extract())

        if provision_list.previous_sibling is not None:
            for node in nodes_to_insert:
                provision_list.previous_sibling.insert_after(node)
        else:
            for i, node in enumerate(nodes_to_insert):
                provision_list.parent.insert(i, node)
        provision_list.decompose()
    return doc


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
    for header in doc.find_all(lambda tag: tag.name in ('h2', 'h3', 'h4', 'h5', 'h6')):
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
