# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:43:39 2023

@author: nicol

This script will serve as the AWS Lambda handler
that initiates the process of fetching songs from Spotify playlists.
This handler will be triggered by an API Gateway event.
It will read the URIs in the body of the request and enqueue tasks in an SQS queue to process each playlist sequentially.
"""

from common.utils import generate_unique_request_code, is_valid_spotify_playlist_uri

from cloud_services.aws_utilities.aws_state_machine_utils import start_fetch_state_machine

def lambda_handler(event, context):
    # TODO
    # Add url referer check
    
    request_id = generate_unique_request_code()
    
    # Extract playlist URIs from the body of the POST request
    try:
        body = event['body'].replace('"', '') # The body often comes to the lambda as "<body content>"
        playlist_uris = [item.strip() for item in body.split(',')]
        
        # Validate each URI
        for uri in playlist_uris:
            if not is_valid_spotify_playlist_uri(uri.strip()):
                return {
                    'statusCode': 400,
                    'body': f'Bad request: Invalid playlist URI detected - {uri}'
                } 
        
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'Bad request: No playlist URIs provided'
        }  

    # Iterate over playlist URIs and send messages to SQS queue
    req_n_playlists = len(playlist_uris)
    start_fetch_state_machine(request_id, playlist_uris, req_n_playlists)

    return {
        'statusCode': 200,
        'body': '{"request_id": "' + request_id + '"}'
    }