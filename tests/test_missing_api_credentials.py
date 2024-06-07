import unittest
import argparse
from unittest.mock import patch
import cli


class TestMissingApiCredentials(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(file='mock_file.json', key_id=None, api_key=None))
    def test_missing_api_credentials(self, mock_parse_args):
        with self.assertRaises(SystemExit):
            cli.main()


if __name__ == "__main__":
    unittest.main()
