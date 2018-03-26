from unittest import TestCase
from mock import Mock
from .car import Car

class CarTests(TestCase):

    def setUp(self):
        self.car = Car()

    def test_init_car(self):
        self.assertEqual(self.car.speed, 0)

    def test_stop(self):
        # Is directly accessing a private attribute ok?
        self.car.speed = 10
        self.car.stop()
        self.assertEqual(self.car.speed, 0)

    def test__accelerate(self):
        self.car._accelerate()
        self.assertEqual(self.car.speed, 1)

    def test__decelerate_when_moving(self):
        self.car._accelerate() # 1
        self.car._accelerate() # 2
        self.car._decelerate()
        self.assertEqual(self.car.speed, 1)

    def test__decelerate_when_stopped(self):
        self.car._decelerate()
        self.assertEqual(self.car.speed, 0)

    def test_crash_over_100(self):
        self.car.speed = 100
        self.car._accelerate()
        self.assertEqual(self.car.speed, 0)
        self.assertTrue(self.car.destroyed)
