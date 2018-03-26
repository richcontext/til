## Less boilerplate

def func(x):
    return x + 1

# pytest
def test_answer():
    assert func(3) == 5

# unittest
class MyTest(unittest.TestCase):
    def test_answer(self):
        self.assertEqual(func(3), 5)


# unittest
class MyTest(unittest.TestCase):
    def test_bad_jwt_decode(self):
        try:
            jwt_decode_handler('abc1234')
        except jwt.DecodeError:
            self.assertRaises(jwt.DecodeError)

# pytest
@pytest.mark.xfail(raises=jwt.DecodeError)
def test_bad_jwt_decode():
    jwt_decode_handler('abc1234')


#####


try:
    import mock
except ImportError:
    from unittest import mock

import unittest

from square import Square

class TestClass(unittest.TestCase):

       @mock.patch('__main__.Square') # depends in witch from is run
       def test_mocking_instance(self, mocked_instance):
           mocked_instance = mocked_instance.return_value
           mocked_instance.calculate_area.return_value = 1
           sq = Square(100)
           self.assertEquals(sq.calculate_area(), 1)


       def test_mocking_classes(self):
           sq = Square
           sq.calculate_area = mock.MagicMock(return_value=1)
           self.assertEquals(sq.calculate_area(), 1)

       @mock.patch.object(Square, 'calculate_area')
       def test_mocking_class_methods(self, mocked_method):
           mocked_method.return_value = 20
           self.assertEquals(Square.calculate_area(), 20)

####
# pytest

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from square import Square

def test_mocking_class_methods(monkeypatch):
    monkeypatch.setattr('test_class_pytest.Square.calculate_area', lambda: 1)
    assert Square.calculate_area() ==  1


def test_mocking_classes(monkeypatch):
    monkeypatch.setattr('test_class_pytest.Square', MagicMock(Square))
    sq = Square
    sq.calculate_area.return_value = 1
    assert sq.calculate_area() ==  1
