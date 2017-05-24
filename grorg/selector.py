from PyOrgMode import PyOrgMode
import re


class Selector:
    """ Class containing a path that specifies how to navigate the org-mode document. """

    def __init__(self, selector, recursive=False):
        """ Parse a document selector from a given string.
        Selectors are a path that specifies how to navigate the org-mode document. """
        self.recursive = recursive
        self.path = [re.compile(part) for part in selector.strip('/').split('/')]

    @staticmethod
    def _header(node):
        return type(node) == PyOrgMode.OrgNode.Element

    def _find_headers_matching(self, considered_nodes, part):
        """ Return a list of headers matching the regex part. """
        considering_nodes = considered_nodes[:]
        result = []
        while len(considering_nodes) > 0:
            node = considering_nodes.pop()
            if not Selector._header(node):
                continue
            elif part.match(node.heading):
                result.append(node)
            else:
                considering_nodes.extend(node.content)
        return result

    def apply(self, document):
        """ Apply a selector to an org mode document. """
        considered_nodes = [document.root]
        for part in self.path:
            considered_nodes = self._find_headers_matching(considered_nodes,
                                                           part)
        return considered_nodes
