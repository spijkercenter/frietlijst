import unittest

from order_repository import anonymize_name


class TestMain(unittest.TestCase):
    def test_anonymize_name(self):
        given = "Alice Bobbington Charlie"
        expected = "Alice B C"
        actual = anonymize_name(given)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
