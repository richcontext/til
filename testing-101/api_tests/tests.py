from unittest import TestCase
import mock
from unittest.mock import Mock
from .client import *

class ApiTests(TestCase):

    def setUp(self):
        self.params = {'q': 'test'}

    def test_integration_call(self):
        res = call_api(self.params).json()
        self.assertEqual(res['args'], self.params)

    @mock.patch('api_tests.client.requests.get')
    def test_isolated_call(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {'args': self.params, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.18.4'}, 'origin': '70.178.89.80', 'url': 'http://httpbin.org/get?q=test'}

        res = call_api(self.params)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['args'], self.params)
