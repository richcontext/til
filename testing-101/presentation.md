# Why test?

---

# Untested code is broken code by definition

### If you don't have a test verifying the functionality of the code, you have no idea if it is broken or not. And if you have no idea if it is broken or not, you might as well assume it is broken.

---

# Given A, Expect B

```py
def multiply(x, y):
    return x * y

def add(a, b):
    return a + b
```

## What should we assert here?

---

```py
from unittest import TestCase
from .math import *

class MathTests(TestCase):

    def setUp(self):
        pass

    def test_multiply(self):
        result = multiply(1, 2)
        self.assertEqual(result, 2)

    def test_add(self):
        result = add(5, 10)
        self.assertEqual(result, 15)
```

## How can we make this more dynamic?

---

```py
from unittest import TestCase
from .math import *
import random

class MathTests(TestCase):

    def setUp(self):
      self.lower = 0
      self.upper = 500000

    def get_number():
      return random.randint(self.lower, self.upper)

    def test_multiply(self):
      a = get_number()
      b = get_number()
      result = multiply(a, b)
      self.assertEqual(result, a * b)

    def test_add(self):
      a = get_number()
      b = get_number()
      result = multiply(a, b)
      self.assertEqual(result, a + b)
```

---

## Use the scientific method when thinking about testing code. An assertion is a hypothesis. Running the test is the experiment.

---

# What kind of tests are there?

## Unit test

Tests an individual unit -- a single function.

---

# What kind of tests are there?

## Unit test

Tests an individual unit -- a single function.

## Integration tests

Tests many functions. A subset or slice of functionality in the whole system.

A unit test of a function uploading a file to s3 mocks the response as 200 no matter what. an integration test actually uploads to s3 and tests the result

---

# What kind of tests are there?

## Unit test

Tests an individual unit -- a single function.

## Integration tests

Tests many functions. A subset or slice of functionality in the whole system.

A unit test of a function uploading a file to s3 mocks the response as 200 no matter what. an integration test actually uploads to s3 and tests the result

## Functional/Acceptance/E2E tests

Tests a complete path of functionality in the system

---

## Always test in isolation. if a test calls any outside services, it is not a real test and is subject to unknown side effects

---

## Always test in isolation. if a test calls any outside services, it is not a real test and is subject to unknown side effects

### API Test example

```py
import requests

def call_api(params):
    return requests.get('http://httpbin.org/get', params)
```

```py
class ApiTests(TestCase):
    def test_integration_call(self):
        params = {'q': 'test'}
        res = call_api(params).json()
        self.assertEqual(res['args'], params)

```

## Why is this bad?

---

```py
import requests

def call_api(params):
    return requests.get('http://httpbin.org/get', params)
```

```py
class ApiTests(TestCase):
  @mock.patch('api_tests.client.requests.get')
  def test_isolated_call(self, mock_get):
      params = {'q': 'test'}

      mock_get.return_value = Mock(status_code=200)
      mock_get.return_value.json.return_value = {'args': params, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4'}, 'origin': '70.178.89.80', 'url': 'http://httpbin.org/get?q=test'}

      res = call_api(params)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(res.json()['args'], params)
```

---

### Amount of effort you put into tests should correlate to the impact of the failure

---

### A single successful test is good, but is testing 1 out of infinity possibilities. Testing known bad cases is arguably more valuable. You really need both.

---

## Regressions

### You should run all tests with every change; not just the tests related to what you are building. If the tests have to run in a set order, theyre not properly isolated. One thing that can help is to use your testing framework to randomize test order at runtime.

---

## Tools That Help Testing

### Mocks (also called a test double.)

* A Test Double is simply another object that conforms to the interface of the required Collaborator, and can be passed in its place. fully replacing a class.

* MagicMock - part of python testing framework. has most magic methods implemented. __lt__, __gt__, __len__, etc

* mocking a return value vs attaching a side effect

---

## Mocks - Return values vs side effects

### Explicitly set a static return value

```py
def test_rm(self, mock_os, mock_path):
  filename = 'thing'
  mock_path.isfile.return_value = True
  self.assertTrue(mock_path.isFile(filename))

```

### How do we test condition of sending in a bad parameter?

---

### Use a side effect


```py
def mock_is_file(arg):
  if isinstance(arg, String):
    return true
  else:
    raise NotARealPathException

def test_bad_rm(self, mock_os, mock_path):
  filename = 'thing'
  mock_path.isfile.side_effect = mock_is_file

  self.assertRaises(mock_path.isFile(filename), NotARealPathException)
```

---

### How do we test this?

```py
import os
import os.path

def rm(filename):
    if os.path.isfile(filename):
        os.remove(filename)
```

---

## Use a Mock

---

```py
import mock
import unittest
from .file_funcs import rm

class RmTestCase(unittest.TestCase):

    @mock.patch('basic_tests.file_funcs.os.path')
    @mock.patch('basic_tests.file_funcs.os')
    def test_rm(self, mock_os, mock_path):
        # set up the mock
        mock_path.isfile.return_value = False

        rm("any path")

        # test that the remove call was NOT called.
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")

        # make the file 'exist'
        mock_path.isfile.return_value = True

        rm("any path")

        mock_os.remove.assert_called_with("any path")
```

---

## Tools That Help Testing

### Stubs - fake objects with pre-programmed behavior

Stubs are just mocks with highly specific and configured return values and side effects. They're both dummy implementations of objects the code under tests interacts with.

### What is the difference between a mock and a stub?

Stubs are like inputs to tests. Stubs provide the condition that prompts the different behavior in your code but they're not the way you verify that behavior. You generally stub things you don't necessarily care about, but you need it to behave in a way to allow the tests to continue.

Mocks are like outputs of code under test. With mocks you have a more generic interface to testing.

You make a stub return a specific value. You use a mock to see what the object actually returns.

Stubs are prescriptive scenarios. Mocks simulate many scenarios.

---

## Tools That Help Testing

Spies - A test spy is an object that records its interaction with other objects throughout the code base. can be done with pythons mock library

```py
mocked_func.assert_called_once_with(arg)
mocked_func.assert_called_with(arg1, arg2, arg3)
mocked_func.assert_not_called()
```

---

## Tools That Help Testing

### Factories - code that generates a test object at runtime.

---

## Factories
## Factory Boy

```py
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username%s' % n)

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = faker.lorem(words=5)

class ClientFactory(BaseModelFactory):
    class Meta:
        model = Client

    name = faker.company_name()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)

```

---

## Factories
### SubFactories

```py
class PublicationAPIActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PublicationAPIActivity

    publication = factory.SubFactory(PublicationFactory)
    retail_platform_page = factory.SubFactory(RetailPlatformPageFactory)
```

---

## Tools That Help Testing

Fixtures - Preset scaffolding of data. you dont change it and its set the same forever

```py
{
   'args':{
      'q':'test'
   },
   'headers':{
      'Accept':'*/*',
      'Accept-Encoding':'gzip, deflate',
      'Connection':'close',
      'Host':'httpbin.org',
      'User-Agent':'python-requests/2.18.4'
   },
   'origin':'70.178.89.80',
   'url':'http://httpbin.org/get?q=test'
}
```

### It will only return this. Every time. Can be brittle.

---

## TDD
  - test driven development
  - write tests first. red/fail
  - write implementation to make the tests pass. green.
  - refactor implementation code to make it better. keep it green

---

## BDD

  - Comes from agile world
  - behavior driven development
  - based off of user story
  - write code to satisfy user story
  - heavily functional testing

---

# Real Example

```py
import jwt
import mock
import rest_framework_jwt
from django.test import TestCase
from rest_framework_jwt.compat import get_user_model
from unittest.mock import Mock
from xena.utils.jwt import jwt_decode_handler
User = get_user_model()


class JwtTests(TestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.email = 'jpueblo@example.com'
        self.user = User.objects.create_user(self.username, self.email)

    @mock.patch('xena.utils.jwt.requests.post')
    def test_good_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = {'token': token}

        decoded_payload = jwt_decode_handler(token)

        self.assertEqual(decoded_payload, payload)

    @mock.patch('xena.utils.jwt.requests.post')
    def test_bad_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=400)
        mock_post.return_value.json.return_value = {"non_field_errors":["Error decoding signature."]}

        try:
            jwt_decode_handler(token)
        except jwt.DecodeError:
            self.assertRaises(jwt.DecodeError)

    @mock.patch('xena.utils.jwt.requests.post')
    def test_expired_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=400)
        mock_post.return_value.json.return_value = {"non_field_errors": ["Signature has expired."]}

        try:
            jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            self.assertRaises(jwt.ExpiredSignatureError)
```

---

## DocTests

```py
def square(x):
    """Return the square of x.

    >>> square(2)
    4
    >>> square(-2)
    4
    """

    return x * x

if __name__ == '__main__':
    import doctest
    doctest.testmod()
```

---

## PyTest

Less boilerplate

```py
# Code under test
def func(x):
    return x + 1

# unittest
class MyTest(unittest.TestCase):
    def test_answer(self):
        self.assertEqual(func(3), 5)

# pytest
def test_answer():
    assert func(3) == 5


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
```

---

# Let's work through testing this class

```py
class Car(object):

    def __init__(self):
        self.color = 'red'
        self.speed = 0

    def _accerate(self):
        self.speed += 1

    def _decelerate(self):
        pass

    def stop(self):
        self.speed = 0

```

---

```py
from unittest import TestCase
from .car import Car

class CarTests(TestCase):

    def setUp(self):
        self.car = Car()

    def test_stop(self):
      pass

    def test_moving_car_stop(self):
      pass

    def test_accelerate(self):
      # Thoughts on this?
      pass

```
