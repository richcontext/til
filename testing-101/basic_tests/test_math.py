from unittest import TestCase
from .math import *
import random

class MathTests(TestCase):
    """Code under test:

    def multiply(x, y):
        return x * y

    def add(a, b):
        return a + b
    """

    def setUp(self):
      self.lower = 0
      self.upper = 500000

    def get_number(self):
      return random.randint(self.lower, self.upper)

    def test_multiply(self):
        result = multiply(1, 2)
        self.assertEqual(result, 2)

    def test_add(self):
        result = add(5, 10)
        self.assertEqual(result, 15)

    def test_multiply_better(self):
      a = self.get_number()
      b = self.get_number()
      result = multiply(a, b)
      self.assertEqual(result, a * b)

    def test_add_better(self):
      a = self.get_number()
      b = self.get_number()
      result = add(a, b)
      self.assertEqual(result, a + b)
