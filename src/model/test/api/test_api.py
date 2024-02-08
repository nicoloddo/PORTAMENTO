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
data = "spotify:playlist:5T54YmcS3PsSghWrqivfms\r\nspotify:playlist:7460eJSzkWMB3VQ2xzACiV\r\nspotify:playlist:2HF1k7XYrLeooG2EYzIYwk\r\nspotify:playlist:7rldaIGrPgeiOVcfeQ5ZjR"

response = requests.post(url, headers=headers, data=json.dumps(data))

# This will print the status code and response body
print(f'Status Code: {response.status_code}')
print(f'Response: {response.json()}')


'''
This is what was received:
{"request_id": "52a34ac4-44cc-4431-9032-3f85e5ef05e9-1707351206", 
 "req_n_playlists": 1, 
 "playlist_uri": "\"\\nspotify:playlist:5T54YmcS3PsSghWrqivfms\\r\\nspotify:playlist:7460eJSzkWMB3VQ2xzACiV\\r\\nspotify:playlist:2HF1k7XYrLeooG2EYzIYwk\\r\\nspotify:playlist:7rldaIGrPgeiOVcfeQ5ZjR\\n\"", 
 "start_index": 0, "batch_size": 100}

One only playlist_uri with wrongly parsed \n and \r

Moreover, the SQS was continuously triggering 4 song fetchers all the time.
'''