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

ask_for_model_id = False
if ask_for_model_id:
    model_id = input("Please enter the model id: ")
else:
    model_id = '7cee9ff4-d496-4b68-b2bc-c3034e5e7cea-1711649889'
node_id = '0'

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
    'model-id': model_id,
    'node-id': node_id
}

response = requests.get(url, headers=headers)

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')

body = json.loads(response.text)

"""
When implementing this in the interface, make an automatic retry until you get
a 200 status code, or until a max number of requests is reached.
"""