# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:25:58 2024

@author: nicol
"""

import requests
import json
from datetime import datetime

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
    model_id = '7d2a491e-5911-4e59-8516-a8c61a52f002-1730918817'
node_id = '0'

headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
    'model-id': model_id,
    'node-id': node_id
}

# Get the pre-signed URL from Lambda
response = requests.get(url, headers=headers)

# Print the initial response
print(f'Lambda Status Code: {response.status_code}')
print(f'Lambda Response: {response.text}')

if response.status_code == 200:
    # Parse the response
    response_data = json.loads(response.text)
    
    # Check expiration
    if datetime.now().timestamp() < response_data['expires_at']:
        # Fetch the actual data using the pre-signed URL
        data_response = requests.get(response_data['url'])
        print(f'\nS3 Data Status Code: {data_response.status_code}')
        
        if data_response.status_code == 200:
            node_data = data_response.json()
            print(f'Node Data: {json.dumps(node_data, indent=4)}')
        else:
            print(f'Failed to fetch data from S3: {data_response.text}')
    else:
        print('Response URL has expired')
else:
    print('Failed to get pre-signed URL from Lambda')

"""
When implementing this in the interface, make an automatic retry until you get
a 200 status code, or until a max number of requests is reached.
"""