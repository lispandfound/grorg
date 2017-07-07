from grorg import property_filter
import time
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
        prop_filter.add_filter(*property_filter.relationship_from('name=Fido'))
        # Test name = Fido filter
        self.assertTrue(prop_filter.apply_filter(self.test_data[0]))
        prop_filter.add_filter(*property_filter.relationship_from('name=Bubbles'))
        # Test name = Fido, name = Bubbles filter (multiple relationships)
        # Fido
        self.assertTrue(prop_filter.apply_filter(self.test_data[0]))
        # Bubbles
        self.assertTrue(prop_filter.apply_filter(self.test_data[1]))
        # Test invalid property filter
        prop_filter.filter_dict.clear()
        prop_filter.add_filter(*property_filter.relationship_from('height>3'))
        self.assertFalse(prop_filter.apply_filter(self.test_data[0]))


class TestRelationships(unittest.TestCase):

    def test_relationships(self):

        test_cases = {
            ('a=Hello', 'Hello'): True,
            ('a>3', 4): True,
            ('a!>3', 4): False,
            ('a~.at', 'Cat'): True,
            ('a!&a;b;c;d', 'e'): True,
            ('a><2017-07-06 Thu>', time.strptime("30 Jun 2017 22:59:60", "%d %b %Y %H:%M:%S")): False
        }

        for relationship_test, expected_result in test_cases.items():
            relationship_string, argument = relationship_test
            prop, relationship = property_filter.relationship_from(relationship_string)
            value = relationship(argument)
            print(f'{relationship_string} held {value} when called with {argument}')
            self.assertEqual(value, expected_result)
            self.assertEqual(prop, 'a')

        _, relationship = property_filter.relationship_from('a&test;1;2;3')
        self.assertTrue(relationship(['test']))
