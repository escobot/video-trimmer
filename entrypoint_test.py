import unittest
from entrypoint import to_seconds


class Entrypoint(unittest.TestCase):

    def test_to_seconds(self):
        self.assertEqual(to_seconds("00:00"), 0)
        self.assertEqual(to_seconds("00:00:00"), 0)
        self.assertEqual(to_seconds("01:00"), 60)
        self.assertEqual(to_seconds("01:01:01"), 3600 + 60 + 1)
        self.assertEqual(to_seconds("1:00"), 60)
        self.assertEqual(to_seconds("1:01:01"), 3600 + 60 + 1)


if __name__ == '__main__':
    unittest.main()
