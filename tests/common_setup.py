import os
import json
import base64
import unittest


class CommonSetup(unittest.TestCase):
    def setUp(self):
        self.mock_key_id = "test_key_id"
        self.mock_api_key = "test_api_key"
        self.mock_file_name = 'mock_file.json'
        self.mock_data = {
            "sender": {"name": "Test Guy", "address": "123 Main St, Anytown"},
            "recipient": {"name": "John Doe", "address": "456 Elm St, Othertown"},
            "items": [{"name": "Item 1", "quantity": 2, "weight": 1.5}]
        }

        with open(self.mock_file_name, 'w') as f:
            json.dump(self.mock_data, f)

        self.mock_response = {
            "trackingNumber": "123456789",
            "labelReference": "label123",
            "provider": "mock_provider"
        }

        self.mock_label_content = base64.b64encode(b"mock pdf content").decode('utf-8')

    def tearDown(self):
        file_paths = [self.mock_file_name, "123456789.pdf", "123456789.log"]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
