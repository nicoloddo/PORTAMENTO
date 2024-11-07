# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:39:23 2024

@author: nicol
"""

import requests
import json

from common.utils import load_env_var

# Get API Key
api_key = load_env_var('API_KEY')

# Build API Gateway URL path
API_BASE_URL = load_env_var('API_BASE_URL')
url = API_BASE_URL + '/cluster'

use_default_model_id = True
if use_default_model_id:
    data_id = load_env_var('DEFAULT_MODEL_ID')
else:
    data_id = input("Please enter the data id: ")

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
    'data-id': data_id
}

# Example data
with open('src/model/test/api/clusterer_api_test_config.json', 'r') as file:
    data = json.load(file)

response = requests.post(url, headers=headers, json=data)

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')


"""
When implementing this in the interface, make an automatic retry until you get
a 200 status code, or until a max number of requests is reached.
"""