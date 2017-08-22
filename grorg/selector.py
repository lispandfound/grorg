from collections import deque
from PyOrgMode import PyOrgMode
import re


def drawer_from(header, name='PROPERTIES'):
    ''' Get properties drawer from given org mode header. Performs a linear
    search through the content for the drawer. '''

    for child in header.content:
        is_drawer = type(child) == PyOrgMode.OrgDrawer.Element
        if is_drawer and child.name == name:
            return child

    return None


def header(node):
    """ Returns True if given node is a header node. """
    return type(node) == PyOrgMode.OrgNode.Element


def node_str(nodes):
    node_str = []
    for node in nodes:
        if not header(node):
            continue
        content = node.content
        node.content = []
        node_str.append(node.output().strip())
        node.content = content
    return node_str


def expand(nodes, recursive=False):
    """ Return a list containing all the children of every node in
    nodes. """
    node_queue = deque(nodes)
    result = []
    while len(node_queue) > 0:
        node = node_queue.popleft()
        if not header(node):
            continue
        elif recursive is True:
            node_queue.extendleft(reversed(node.content))
        result.append(node)
    return result


def parse_selector(selector):
    """ Parse a document selector from a given string.
    Selectors are a path that specifies how to navigate the
    org-mode document. """
    recursive = False

    if selector[:2] == '//':
        recursive = True

    path = [re.compile(part) for part in selector.strip('/').split('/')]
    return path, recursive


def apply_selector(selector, document):
    """ Apply a selector to an org mode document. """

    path, recursive = parse_selector(selector)

    considered_nodes = document.root.content
    for part in path:

        considered_nodes = expand(considered_nodes, recursive=recursive)

        def predicate(node):
            return re.match(part, node.heading)

        considered_nodes = [node for node in considered_nodes if predicate(node)]
        recursive = False
    return considered_nodes
