import os
import sys
import unittest

# from ralf import ralf


class Test_ralf(unittest.TestCase):
    """
    Test the various functionalities of ralf.
    """

    @classmethod
    def setUpClass(self):
        return

    def test_placeholder(self):
        """
        """
        self.assertTrue(1+1 == 2)


if __name__ == '__main__':
    unittest.main()
