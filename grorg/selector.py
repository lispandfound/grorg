from collections import deque
from PyOrgMode import PyOrgMode
import re


def find_headers_matching(node, predicate, recursive=False):
    """ Return a list of all sub-nodes of node (or list of nodes)
    matching a predicate. If the recursive flag is set, consider all
    sub-nodes recursively. """
    if type(node) == list:
        node_stack = deque(node)
    else:
        node_stack = deque(node.content)
    result = []
    while len(node_stack) > 0:
        child = node_stack.pop()
        if not header(child):
            continue
        elif predicate(child):
            result.append(child)
        else:
            node_stack.extendleft(child.content)
    return result


def header(node):
    """ Returns True if given node is a header node. """
    return type(node) == PyOrgMode.OrgNode.Element


def expand(nodes, recursive=False):
    """ Return a list containing all the children of every node in
    nodes. """
    result = []
    node_queue = deque(nodes)

    while len(node_queue) > 0:
        node = node_queue.popleft()
        if not header(node):
            continue
        elif recursive:
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

    considered_nodes = [document.root]
    for part in path:

        considered_nodes = expand(considered_nodes)

        def predicate(node):
            return re.match(part, node.heading)

        considered_nodes = find_headers_matching(considered_nodes,
                                                 predicate,
                                                 recursive=recursive)
    return considered_nodes
