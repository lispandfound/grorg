from PyOrgMode import PyOrgMode
import re


class Selector:
    """ Class containing a path that specifies how to navigate the org-mode document. """

    def __init__(self, selector):
        """ Parse a document selector from a given string.
        Selectors are a path that specifies how to navigate the org-mode document. """
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
        """ Return a list containing all the children of every node in nodes. """
        children = []
        for node in nodes:
            if Selector._header(node):
                children.extend(node.content)
        return children

    def _find_headers_matching(self, considered_nodes, part, recursive=False):
        """ Return a list of headers matching the regex part. """
        considering_nodes = considered_nodes[:]
        result = []
        while len(considering_nodes) > 0:
            node = considering_nodes.pop()
            if not Selector._header(node):
                continue
            elif part.match(node.heading):
                result.append(node)
            elif recursive:
                considering_nodes.extend(node.content)
        return result

    def apply(self, document):
        """ Apply a selector to an org mode document. """
        considered_nodes = [document.root]
        for part in self.path:

            considered_nodes = Selector._expand(considered_nodes)

            considered_nodes = self._find_headers_matching(considered_nodes,
                                                           part,
                                                           recursive=self.recursive)
        return considered_nodes
