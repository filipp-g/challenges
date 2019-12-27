#!/usr/bin/env python
""" An xml parser to validate given graph xml """

import xml.etree.ElementTree as ET

# can be file in project folder, or url
xml_file = 'sample.xml'

# boo on http and poor url validation, for demo purposes only
if xml_file.startswith('http'):
    import ssl
    from urllib.request import build_opener as opener
    # dirty hack to not bother with ssl certs for demo, not for production!
    ssl._create_default_https_context = ssl._create_unverified_context
    xml_file = opener().open(xml_file)

try:
    root = ET.parse(xml_file).getroot()
    if root.tag != 'graph':
        quit('supplied xml is not for graph\nquitting.')
except ET.ParseError as e:
    quit(f'parse error - {e}\nquitting.')


graph_id = root.find('id')
graph_name = root.find('name')
graph_nodes = root.find('nodes')
graph_edges = root.find('edges')

node_nodes = graph_nodes.findall('node')
edge_nodes = graph_edges.findall('node')
all_nodes = node_nodes + edge_nodes

unique_node_ids = []


def tag_is_none_or_blank(tag):
    return tag is None or not tag.text or not tag.text.strip()


def get_node_id(node):
    return None if node.find('id') is None else node.find('id').text


def get_unique_node_ids():
    ids = [x for x in (get_node_id(y) for y in all_nodes) if x is not None]
    return set(ids)


def all_nodes_have_valid_unique_ids():
    # can certainly think of more robust ways to do this,
    # but good enough for this purpose.
    return len(unique_node_ids) == len(all_nodes)


def all_edge_nodes_are_valid():
    for node in edge_nodes:
        from_tags = [x.text for x in node.findall('from')]
        to_tags = [x.text for x in node.findall('to')]
        if (len(from_tags) != 1 or len(to_tags) != 1 or
                not {from_tags[0], to_tags[0]}.issubset(unique_node_ids)):
            return False
    return True


if tag_is_none_or_blank(graph_id):
    quit('graph must have an <id> tag.\nquitting.')

if tag_is_none_or_blank(graph_name):
    quit('graph must have a <name> tag.\nquitting.')

if len(node_nodes) == 0:
    quit('graph must have at least one <node> in <nodes> group.\nquitting.')

unique_node_ids = get_unique_node_ids()

if not all_nodes_have_valid_unique_ids():
    quit('all graph <node>s must have valid and unique <id>s.\nquitting.')

if not all_edge_nodes_are_valid():
    quit('edge <node>s have incorrect <to> and <from> tags.\nquitting.')

print('graph xml has been parsed and passed all validation.')
