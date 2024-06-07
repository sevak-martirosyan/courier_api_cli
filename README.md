# Courier API Command Line Interface

## Name
Borderless360 Test Assignment - Courier API Command Line Interface

## Description
This program working with a sandbox environment of a real courier API - Machool and creating a mock shipment.

1. Program takes the JSON sample file and credentials as an input
2. Program invokes an API Client class object which takes the specified credentials and has its interface tied to the requests it can make
3. API client sends a POST request to the Rates endpoint to determine the cheapest carrier service
4. API Client sends a POST request to the Shipments endpoint to create a shipment with the found service
5. Program saves the label received from the shipment creation as a PDF file in the same folder as the JSON sample with the filename of the tracking number of the created shipment (example: 232123512.pdf)
6. Program saves the full request/response data as a .log file in the same folder as the JSON sample (same naming as the PDF file - 232123512.log)

## Installation
The program tested in a Linux environment (Ubuntu 18.04).

Do the following steps to make a working environment.

1. sudo apt install python3.10
2. sudo apt install python3.10-venv
3. git clone https://gitlab.com/sevakm/courier_api_cli.git
4. cd ./courier_api_cli
5. python3.10 -m venv venv
6. . venv/bin/activate
7. pip install requests

Done!

## Usage
. venv/bin/activate (if venv not active).

Run the script.
 - python3.10 cli.py create_shipment -f test_machool_order_data.json -keyid bCahFZHQc3 -apikey 645744e8-a047-421a-b882-7d2471f6bab5

Run some unittests.
 - python3.10 -m unittest discover -s tests

## Author
Sevak Martirosyan

