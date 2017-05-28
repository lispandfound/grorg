import property_filter
import unittest


class Pet:
    """ Dummy class to test property filter on. """

    def __init__(self, name, cost, age, toys=[]):

        self.name = name
        self.cost = cost
        self.age = age


class TestPropertyFilter(unittest.TestCase):
    """ Class to test property filter from the property_filter module. """

    def setUp(self):
        self.test_data = [
            Pet('Fido', 150, 1),
            Pet('Bubbles', 10, 0),
            Pet('Tiger', 100, 3),
            Pet('Rover', 100, 2, toys=set('Ball'))
        ]

    def test_add_filter(self):
        prop_filter = property_filter.PropertyFilter()
        prop_filter.add_filter('name', 'Fido')
        self.assertEqual(prop_filter.filter_dict, {'name': ['Fido']})

    def test_apply_filter(self):
        prop_filter = property_filter.PropertyFilter()
        prop_filter.add_filter('name',
                               property_filter.relationship_from('=Fido'))
        # Test name = Fido filter
        self.assertTrue(prop_filter.apply_filter(self.test_data[0]))
        prop_filter.add_filter('name',
                               property_filter.relationship_from('=Bubbles'))
        # Test name = Fido, name = Bubbles filter (multiple relationships)
        # Fido
        self.assertTrue(prop_filter.apply_filter(self.test_data[0]))
        # Bubbles
        self.assertTrue(prop_filter.apply_filter(self.test_data[1]))
        # Test invalid property filter
        prop_filter.filter_dict.clear()
        prop_filter.add_filter('height',
                               property_filter.relationship_from('>3'))
        self.assertFalse(prop_filter.apply_filter(self.test_data[0]))


class TestRelationships(unittest.TestCase):
    def setUp(self):
        self.test_cases = {
            ('=Hello', 'Hello'): True,
            ('>3', '4'): True,
            ('!>3', '4'): False,
            ('=.at', 'Cat'): True,
            ('}test', frozenset(set(['test']))): True,
            ('!}a', frozenset(set(['b', 'c', 'd']))): True
        }

    def test_relationships(self):
        for relationship_test, expected_result in self.test_cases.items():
            relationship_string, argument = relationship_test
            relationship = property_filter.relationship_from(relationship_string)
            self.assertEqual(relationship(argument), expected_result)
