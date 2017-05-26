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
        child = node_stack.popleft()
        if not Selector._header(child):
            continue
        elif predicate(child):
            result.append(child)
        elif recursive:
            node_stack.extend(child.content)
    return result


class Selector:
    """ Class containing a path that specifies how to navigate the
    org-mode document. """

    def __init__(self, selector):
        """ Parse a document selector from a given string.
        Selectors are a path that specifies how to navigate the
        org-mode document. """
        self.recursive = False
        if selector[:2] == '//':
            self.recursive = True
        self.path = [re.compile(part) for part in selector.strip('/').split('/')]

    @staticmethod
    def _header(node):
        """ Returns True if given node is a header node. """
        return type(node) == PyOrgMode.OrgNode.Element

    @staticmethod
    def _expand(nodes):
        """ Return a list containing all the children of every node in
        nodes. """
        children = []
        for node in nodes:
            if Selector._header(node):
                children.extend(node.content)
        return children

    def apply(self, document):
        """ Apply a selector to an org mode document. """
        considered_nodes = [document.root]
        for part in self.path:

            considered_nodes = Selector._expand(considered_nodes)

            def predicate(node):
                return re.match(part, node.heading)

            considered_nodes = find_headers_matching(considered_nodes,
                                                     predicate,
                                                     recursive=self.recursive)
        return considered_nodes
