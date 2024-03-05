# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:25:58 2024

@author: nicol
"""

import requests
import json

from common.utils import load_env_var

# Get API Key
api_key = load_env_var('API_KEY')

# Build API Gateway URL path
API_BASE_URL = load_env_var('API_BASE_URL')
url = API_BASE_URL + '/nav'

model_id = '' # Substitute this with the request id
node_id = '0002'

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
    'model-id': model_id,
    'node-id': node_id
}

# Example data
with open('./clusterer_api_test_config.json', 'r') as file:
    data = json.load(file)

response = requests.get(url, headers=headers)

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')

body = json.loads(response.text)