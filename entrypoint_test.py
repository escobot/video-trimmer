import unittest
from entrypoint import to_seconds, seconds_to_h_m_s


class Entrypoint(unittest.TestCase):

    def test_to_seconds(self):
        self.assertEqual(to_seconds("00:00"), 0)
        self.assertEqual(to_seconds("00:00:00"), 0)
        self.assertEqual(to_seconds("01:00"), 60)
        self.assertEqual(to_seconds("01:01:01"), 3600 + 60 + 1)
        self.assertEqual(to_seconds("1:00"), 60)
        self.assertEqual(to_seconds("1:01:01"), 3600 + 60 + 1)

    def test_seconds_to_h_m_s(self):
        self.assertEqual(seconds_to_h_m_s(0), "00:00:00")
        self.assertEqual(seconds_to_h_m_s(60), "00:01:00")
        self.assertEqual(seconds_to_h_m_s(60 * 60), "01:00:00")
        self.assertEqual(seconds_to_h_m_s(60 * 60 + 60 + 1), "01:01:01")


if __name__ == '__main__':
    unittest.main()
