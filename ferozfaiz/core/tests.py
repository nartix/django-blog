from django.test import TestCase

# Create your tests here.
import unittest
from core.utils.tokenizer import Tokenizer2


class TestTokenizer2(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer2(salt='salt', sep=':', key='key')

    def test_build_object(self):
        data, token, max_age = self.tokenizer._build_object(
            'test', token='token', max_age=3600)
        self.assertEqual(data, 'test')
        self.assertEqual(token, 'token')
        self.assertEqual(max_age, 3600)

    def test_handle_args_and_kwargs(self):
        data = self.tokenizer._handle_args_and_kwargs(('test',), {})
        self.assertEqual(data, 'test')

        data = self.tokenizer._handle_args_and_kwargs((), {'key': 'value'})
        self.assertEqual(data, {'key': 'value'})

        data = self.tokenizer._handle_args_and_kwargs(('test', 'test2'), {})
        self.assertEqual(data, ['test', 'test2'])

    def test_encode(self):
        encoded = self.tokenizer.encode('test')
        self.assertIsInstance(encoded, str)

    def test_decode(self):
        encoded = self.tokenizer.encode('test')
        decoded = self.tokenizer.decode('test', token=encoded, max_age=3600)
        self.assertIsInstance(decoded, str)

        encoded1 = self.tokenizer.encode(pk=1, email='test')
        decoded1 = self.tokenizer.decode(
            pk=1, email='test', token=encoded1, max_age=3600)
        self.assertIsInstance(decoded1, str)

    def test_remove_data(self):
        token = 'test:token'
        removed = self.tokenizer.remove_data(token)
        self.assertEqual(removed, 'token')

    def test_encode_base64(self):
        encoded = self.tokenizer.encode_base64('test')
        self.assertIsInstance(encoded, str)


if __name__ == '__main__':
    unittest.main()
