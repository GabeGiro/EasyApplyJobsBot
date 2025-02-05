import unittest
import utils.utils as utils

class TestUtility(unittest.TestCase):
    def test_progress_matches(self):
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(1, 10, 10.0))
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(5, 10, 50.0))
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(10, 10, 100.0))
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(3, 4, 75.0))
    
    def test_progress_does_not_match(self):
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(1, 10, 15.0))
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(5, 10, 55.0))
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(10, 10, 90.0))
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(3, 4, 70.0))
    
    def test_progress_edge_cases(self):
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(0, 10, 0.0))
        self.assertTrue(utils.progressMatchesExpectedApplicationPage(10, 10, 100.0))
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(0, 10, 1.0))
        self.assertFalse(utils.progressMatchesExpectedApplicationPage(10, 10, 99.0))

if __name__ == '__main__':
    unittest.main()