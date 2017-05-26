class PropertyFilter:
    """ The property filter class checks a range of properties of an
    object have specified values. """

    def __init__(self, filter_dict={}):
        """ Initialization of filter class. """
        self.filter_dict = filter_dict

    def add_filter(self, filter_property, filter_value):
        """ Add another filter property to the filter object. """
        self.filter_dict[filter_property] = filter_value

    def apply_filter(self, source):
        """ Apply a filter to a given object (source). Returns True if
        all properties of the filter match the given object. """
        for filter_property, property_value in self.filter_dict:
            if not hasattr(source, filter_property):
                return False
            elif getattr(source, filter_property) != property_value:
                return False
        return True
