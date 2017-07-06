import re
from PyOrgMode import PyOrgMode


def parse_value(value):
    ''' Parse a string into a value depending on it's contents. '''
    match_integer = re.compile('^\d+$')

    if len(value) > 1:
        # Short for list or set
        return value
    elif match_integer.match(value):
        # Return true if value is an integer
        return int(value)
    try:
        # Use PyOrgMode date parsing because it is more robust than anything I
        # could come up with.
        date = PyOrgMode.OrgDate(value=value)
        return date.value
    except Exception:
        # Please forgive me for the sins I have committed.
        pass
    return value


class RelationshipParseError(Exception):
    pass


KEY_VALUE_RE = re.compile('^(?P<property>\w+)(?P<invert>!)?(?P<relationship>=|>|<|{|~|&)(?P<value>.*)?$')


def relationship_from(relationship_string):
    """ Build a relationship (an expression of some (dis)similarity
    between two values) from a string.
    Relationships include:
    - '=', equal.
    - '~', regex matching.
    - '>', greater than.
    - '<', less than.
    - '&', membership (of lists or sets).
    All relationships can be inverted with a '!'
    """

    match = re.match(KEY_VALUE_RE, relationship_string)
    if not match:
        raise RelationshipParseError()
    else:
        relationship_property = match.group('property')
        value = match.group('value')
        invert = match.group('invert')

        invert_relationship = False
        if invert is not None:
            invert_relationship = True
            relationship_string = relationship_string[1:]

        relationship_operator = match.group('relationship')
        relationship_rhs = parse_value(value.split(';'))

        def gt_mapping(lhs):
            return lhs > relationship_rhs

        def lt_mapping(lhs):
            return not gt_mapping(lhs)

        def membership_mapping(lhs):
            relationship_set = set(relationship_rhs)
            if type(lhs) == list:
                return set(lhs) & relationship_set
            else:
                return lhs in relationship_set

        def equal_mapping(lhs):
            return str(lhs) == relationship_rhs

        def regex_mapping(lhs):
            return re.compile(value).match(lhs) is not None

        relationship_mapping = {
            '=': equal_mapping,
            '>': gt_mapping,
            '<': lt_mapping,
            '&': membership_mapping,
            '~': regex_mapping
        }

        mapping = relationship_mapping[relationship_operator]

        def apply_mapping(lhs):
            relationship_holds = mapping(lhs)
            if invert_relationship:
                return not relationship_holds
            else:
                return relationship_holds

        return relationship_property, apply_mapping


class PropertyFilter:
    """ The property filter class checks a range of properties of an
    object have specified values. """

    def __init__(self, initial_filter_dict=None):
        """ Initialization of filter class. """
        self.filter_dict = initial_filter_dict or {}

    def add_filter(self, filter_property, filter_value):
        """ Add another filter property to the filter object. """
        current_value = self.filter_dict.get(filter_property, [])
        current_value.append(filter_value)
        self.filter_dict[filter_property] = current_value

    def apply_filter(self, source):
        """ Apply a filter to a given object (source). Returns True if
        all properties of the filter match the given object. """
        for filter_property, relationships in self.filter_dict.items():
            if not hasattr(source, filter_property):
                return False
            lhs_property = getattr(source, filter_property)
            relationships_hold = any(relationship(lhs_property)
                                     for relationship in relationships)
            if not relationships_hold:
                return False

        return True
