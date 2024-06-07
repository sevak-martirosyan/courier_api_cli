import os
import sys
import time
import json
import base64
import argparse
import requests


class MachoolApiClient:
    def __init__(self, key_id, api_key):
        self.headers = {
            "x-key-id": key_id,
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.sandbox.machool.com/external/api/v1"

    def get_cheapest_service(self, shipment_data):
        url = f"{self.base_url}/rates"
        response = requests.post(url, headers=self.headers, json=shipment_data)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to get rates: {response_data}")

        rates = response_data.get("rates", [])
        if not rates:
            raise Exception("No rates found in the response")

        # Find the cheapest service
        return min(rates, key=lambda x: x["totalPrice"])

    def create_shipment(self, shipment_data):
        url = f"{self.base_url}/shipments"
        response = requests.post(url, headers=self.headers, json=shipment_data)
        response_data = response.json()

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create shipment: {response_data}")

        return response_data

    def fetch_label(self, provider, label_reference):
        url = f"{self.base_url}/documents"
        params = {
            "provider": provider,
            "labelReference": label_reference,
            "type": "main"
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Failed to fetch label: {response.text}")
            return None


def main():
    parser = argparse.ArgumentParser(description="Create a shipment using Machool API")
    parser.add_argument('create_shipment', help="Create a shipment")
    parser.add_argument('-f', '--file', required=True, help="Path to the JSON sample file")
    parser.add_argument('-keyid', '--key-id', required=True, help="Machool API Key ID")
    parser.add_argument('-apikey', '--api-key', required=True, help="Machool API Key")

    args = parser.parse_args()

    if not args.key_id or not args.api_key:
        print("Error: Missing API credentials")
        sys.exit(1)

    with open(args.file, 'r') as file:
        shipment_data = json.load(file)

    client = MachoolApiClient(args.key_id, args.api_key)

    print("Getting the cheapest service...")
    cheapest_service = client.get_cheapest_service(shipment_data)

    # Update shipment data with the selected service
    shipment_data["serviceName"] = cheapest_service["serviceName"]
    shipment_data["provider"] = cheapest_service["provider"]
    shipment_data["serviceCode"] = cheapest_service["serviceCode"]

    print("Creating shipment...")
    shipment_response = client.create_shipment(shipment_data)

    tracking_number = shipment_response.get("trackingNumber")
    label_reference = shipment_response.get("labelReference")

    if not tracking_number or not label_reference:
        print("Error: Missing tracking number or label reference in the shipment response")
        return

    print(f"Provider: {cheapest_service['provider']}")
    print(f"Label Reference: {label_reference}")
    print("Waiting for 5 seconds before fetching the label...")
    time.sleep(5)

    label_content = client.fetch_label(cheapest_service["provider"], label_reference)

    if label_content:
        label_path = os.path.join(os.path.dirname(args.file), f"{tracking_number}.pdf")
        with open(label_path, "wb") as label_file:
            label_file.write(base64.b64decode(label_content))
        print(f"Label saved as {label_path}")
    else:
        print("No label content found in the response")

    log_path = os.path.join(os.path.dirname(args.file), f"{tracking_number}.log")
    with open(log_path, "w") as log_file:
        json.dump({
            "request": shipment_data,
            "response": shipment_response
        }, log_file, indent=4)

    print(f"Shipment created successfully. Log saved as {log_path}")


if __name__ == "__main__":
    main()
