import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):
    cal = Calculator()
    param_add = [(1, 2, 3), (2, 4, 6), (1, 9, 10),
                 (2, 5, 7), (6, 3, 9)]
    param_divide = [(3, 1, 3), (4, 2, 2), (50, 5, 10),
                    (66, 2, 33), (78, 13, 6)]
    param_sqrt = [(4, 2), (81, 9), (625, 25),
                  (841, 29), (121, 11)]
    param_exp = [(4, math.exp(4)), (81, math.exp(81)),
                 (625, math.exp(625)), (41, math.exp(41)), (13, math.exp(13))]

    def test_add(self):
        for p1, p2, p3 in self.param_add:
            with self.subTest():
                self.assertEqual(self.cal.add(p1, p2), p3)
        self.assertRaises(TypeError, self.cal.add, '1', 2)
        pass

    def test_divide(self):
        for p1, p2, p3 in self.param_divide:
            with self.subTest():
                self.assertEqual(self.cal.divide(p1, p2), p3)
        self.assertRaises(ZeroDivisionError, self.cal.divide, 13, 0)
        pass

    def test_sqrt(self):
        for p1, p2 in self.param_sqrt:
            with self.subTest():
                self.assertEqual(self.cal.sqrt(p1), p2)
        self.assertRaises(ValueError, self.cal.sqrt, -4)
        pass

    def test_exp(self):
        for p1, p2 in self.param_exp:
            with self.subTest():
                self.assertEqual(self.cal.exp(p1), p2)
        self.assertRaises(TypeError, self.cal.exp, None)
        pass


if __name__ == '__main__':
    unittest.main()
