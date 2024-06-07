import os
import unittest
import argparse
from unittest.mock import patch, MagicMock
import cli
from tests.common_setup import CommonSetup


class TestSuccessfulShipmentCreation(CommonSetup):

    @patch('cli.requests.post')
    @patch('cli.requests.get')
    def test_successful_shipment_creation(self, mock_get, mock_post):
        mock_post.side_effect = [
            MagicMock(status_code=200, json=MagicMock(return_value={"rates": [
                {"serviceName": "test_service", "provider": "test_provider", "serviceCode": "test_code",
                 "totalPrice": 10}]})),
            MagicMock(status_code=201, json=MagicMock(return_value=self.mock_response))
        ]
        mock_get.return_value = MagicMock(status_code=200,
                                          json=MagicMock(return_value={"data": self.mock_label_content}))

        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(file=self.mock_file_name, key_id=self.mock_key_id,
                                                   api_key=self.mock_api_key)):
            cli.main()

        self.assertTrue(os.path.exists("123456789.pdf"))
        self.assertTrue(os.path.exists("123456789.log"))


if __name__ == "__main__":
    unittest.main()
