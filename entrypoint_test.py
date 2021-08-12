import unittest
from entrypoint import to_hours, to_seconds


class Entrypoint(unittest.TestCase):

    def test_to_hours(self):
        self.assertEqual(to_hours("00:00"), "00:00:00")
        self.assertEqual(to_hours("10:01"), "00:10:01")
        self.assertEqual(to_hours("01:00:00"), "01:00:00")
        self.assertEqual(to_hours("01:10:01"), "01:10:01")
        self.assertEqual(to_hours("1:00:00"), "1:00:00")
        self.assertEqual(to_hours("1:10:01"), "1:10:01")

    def test_to_seconds(self):
        self.assertEqual(to_seconds("00:00"), 0)
        self.assertEqual(to_seconds("00:00:00"), 0)
        self.assertEqual(to_seconds("01:00"), 60)
        self.assertEqual(to_seconds("01:01:01"), 3600 + 60 + 1)
        self.assertEqual(to_seconds("1:00"), 60)
        self.assertEqual(to_seconds("1:01:01"), 3600 + 60 + 1)


if __name__ == '__main__':
    unittest.main()
