import jwt
import mock
import rest_framework_jwt
from django.test import TestCase
from rest_framework_jwt.compat import get_user_model
from unittest.mock import Mock
from myapp.utils.jwt import jwt_decode_handler
User = get_user_model()


class JwtTests(TestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.email = 'jpueblo@example.com'
        self.user = User.objects.create_user(self.username, self.email)

    @mock.patch('myapp.utils.jwt.requests.post')
    def test_good_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.json.return_value = {'token': token}

        decoded_payload = jwt_decode_handler(token)

        self.assertEqual(decoded_payload, payload)

    @mock.patch('myapp.utils.jwt.requests.post')
    def test_bad_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=400)
        mock_post.return_value.json.return_value = {"non_field_errors":["Error decoding signature."]}

        try:
            jwt_decode_handler(token)
        except jwt.DecodeError:
            self.assertRaises(jwt.DecodeError)

    @mock.patch('myapp.utils.jwt.requests.post')
    def test_expired_jwt_decode(self, mock_post):
        payload = rest_framework_jwt.utils.jwt_payload_handler(self.user)
        token = rest_framework_jwt.utils.jwt_encode_handler(payload)

        mock_post.return_value = Mock(status_code=400)
        mock_post.return_value.json.return_value = {"non_field_errors": ["Signature has expired."]}

        try:
            jwt_decode_handler(token)
        except jwt.ExpiredSignatureError:
            self.assertRaises(jwt.ExpiredSignatureError)
