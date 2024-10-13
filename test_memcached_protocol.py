

import unittest
from memcached_protocol import serialize_storage_command, serialize_get_command, deserialize_response, deserialize_get_response

class TestMemcachedProtocol(unittest.TestCase):

    def test_serialize_storage_command(self):
        command = serialize_storage_command('set', 'mykey', 0, 60, 5, 'hello')
        expected = "set mykey 0 60 5\r\nhello\r\n"
        self.assertEqual(command, expected)

    def test_serialize_storage_command_with_noreply(self):
        command = serialize_storage_command('add', 'testkey', 0, 120, 8, 'testdata', noreply=True)
        expected = "add testkey 0 120 8 noreply\r\ntestdata\r\n"
        self.assertEqual(command, expected)

    def test_serialize_get_command(self):
        command = serialize_get_command(['mykey'])
        expected = "get mykey\r\n"
        self.assertEqual(command, expected)

    def test_deserialize_stored_response(self):
        response = "STORED\r\n"
        result = deserialize_response(response)
        self.assertEqual(result, "STORED")

    def test_deserialize_not_stored_response(self):
        response = "NOT_STORED\r\n"
        result = deserialize_response(response)
        self.assertEqual(result, "NOT_STORED")

    def test_deserialize_get_response(self):
        response = "VALUE mykey 0 5\r\nhello\r\nEND\r\n"
        result = deserialize_get_response(response)
        expected = {"mykey": {"flags": 0, "bytes": 5, "data": "hello"}}
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
