import re


def relationship_from(relationship_string):
    """ Build a relationship (an expression of some (dis)similarity
    between two values) from a string.
    Relationships include:
    - '=', equal (also may include regex).
    - '>', greater than.
    - '<', less than.
    - '{', membership (of lists or sets).
    All relationships can be inverted with a '!'
    """
    invert_relationship = False
    if relationship_string[0] == '!':
        invert_relationship = True
        relationship_string = relationship_string[1:]

    relationship_operator = relationship_string[0]
    relationship_rhs = relationship_string[1:].split(';')

    def gt_mapping(lhs):
        return int(lhs) > int(relationship_rhs[0])

    def lt_mapping(lhs):
        return not gt_mapping(lhs)

    def membership_mapping(lhs):
        relationship_set = set(relationship_rhs)
        if type(lhs) == list:
            return set(lhs) & relationship_set
        else:
            return lhs in set(relationship_rhs)

    def equal_mapping(lhs):
        relationship_rx = re.compile(relationship_rhs[0])
        return relationship_rx.match(lhs) is not None

    relationship_mapping = {
        '=': equal_mapping,
        '>': gt_mapping,
        '<': lt_mapping,
        '{': membership_mapping
    }

    mapping = relationship_mapping[relationship_operator]

    def apply_mapping(lhs):
        relationship_holds = mapping(lhs)
        if invert_relationship:
            return not relationship_holds
        else:
            return relationship_holds

    return apply_mapping


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