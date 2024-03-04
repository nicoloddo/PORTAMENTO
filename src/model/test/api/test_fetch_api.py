# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 21:49:20 2024

@author: nicol
"""

import requests
import json

# API Gateway URL
url = ''

api_key = input("Enter the API key:")

# Replace with the appropriate headers, including the API key
headers = {
    'x-api-key': api_key,  # Only include this if your API requires an API key
    'Content-Type': 'application/json'
}

# Example data
data = "spotify:playlist:5T54YmcS3PsSghWrqivfms,spotify:playlist:7460eJSzkWMB3VQ2xzACiV,spotify:playlist:2HF1k7XYrLeooG2EYzIYwk,spotify:playlist:7rldaIGrPgeiOVcfeQ5ZjR"

response = requests.post(url, headers=headers, data=json.dumps(data))

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')