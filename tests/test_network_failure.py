import unittest
import argparse
from unittest.mock import patch
import requests
import cli
from tests.common_setup import CommonSetup


class TestNetworkFailure(CommonSetup):

    @patch('cli.requests.post', side_effect=requests.exceptions.ConnectionError)
    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(file='mock_file.json', key_id='mock_key_id', api_key='mock_api_key'))
    def test_network_failure(self, mock_parse_args, mock_requests_post):
        with self.assertRaises(requests.exceptions.ConnectionError):
            cli.main()


if __name__ == "__main__":
    unittest.main()
