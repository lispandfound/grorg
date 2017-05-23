from org import parser
import re

class Selector:
    """ Class containing a path that specifies how to navigate the org-mode document. """

    def __init__(self, selector, recursive=False):
        """ Parse a document selector from a given string.
        Selectors are a path that specifies how to navigate the org-mode document. """
        self.recursive = recursive
        self.path = selector.strip('/').split('/')

    def apply(self, document):
        """ Apply a selector to an org mode document. """
        cur_level = document

        for part in self.path:
