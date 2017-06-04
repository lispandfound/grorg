from PyOrgMode import PyOrgMode
import re
import selector
import unittest


class TestSelector(unittest.TestCase):
    def setUp(self):
        self.org_file = PyOrgMode.OrgDataStructure()
        self.org_file.load_from_file('./tests/test.org')

    def test_parse_selector(self):
        test_selector = {
            '//Rel': (['Rel'], True),
            '/Abs': (['Abs'], False),
            '/Nested/Path': (['Nested', 'Path'], False),
            '//Rel/Nested/Path': (['Rel', 'Nested', 'Path'], True)
        }

        for test_selector, expected_result in test_selector.items():
            path, recursive = expected_result
            path = [re.compile(part) for part in path]
            result = selector.parse_selector(test_selector)
            print('Comparing {result} to {expected_result}')
            self.assertEqual(result, (path, recursive))

    def test_apply_selector(self):
        test_selector = {
            '/Test #1': ['Test #1'],
            '/Test #2': ['Test #2'],
            '/Test #\d': ['Test #1', 'Test #2'],
            '//Rel #1': ['Rel #1']
        }

        for test_selector, expected_result in test_selector.items():
            result = selector.apply_selector(test_selector, self.org_file)
            result = [node.heading for node in result]
            print(f'Comparing {result} to {expected_result}')
            self.assertEqual(result, expected_result)
