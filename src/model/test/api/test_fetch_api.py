# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 21:49:20 2024

@author: nicol
"""

import requests
import json

from common.utils import load_env_var

# Get API Key
api_key = load_env_var('API_KEY')

# Build API Gateway URL path
API_BASE_URL = load_env_var('API_BASE_URL')
url = API_BASE_URL + '/fetch'


# Replace with the appropriate headers, including the API key
headers = {
    'x-api-key': api_key,  # Only include this if your API requires an API key
    'Content-Type': 'application/json'
}

# Example data
#data = "spotify:playlist:5T54YmcS3PsSghWrqivfms,spotify:playlist:7460eJSzkWMB3VQ2xzACiV,spotify:playlist:2HF1k7XYrLeooG2EYzIYwk,spotify:playlist:7rldaIGrPgeiOVcfeQ5ZjR"
data = "spotify:playlist:69fEt9DN5r4JQATi52sRtq" # Sound of Everything (6430 songs)

response = requests.post(url, headers=headers, data=json.dumps(data))

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.text}')

# Parse the JSON response into a dictionary
data = json.loads(response.text)

# Access the value associated with 'request_id'
request_id = data['request_id']


"""
When implementing this in the interface, make an automatic retry until you get
a 200 status code, or until a max number of requests is reached.
Note though, in this step, even a 200 status code might not mean that the fetching was completed
because there might have been an error during the step machine execution.
Thus, before starting the next step (clustering) check if there is a valid data.csv in the
request id bucket. If not, retry this.
"""