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

from cloud_services.aws_utilities.aws_sqs_utils import enqueue_playlist

def lambda_handler(event, context):
    request_id = generate_unique_request_code()
    
    # Extract playlist URIs from the body of the POST request
    try:
        body = event['body']
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
    for uri in playlist_uris:
        enqueue_playlist(uri, request_id, req_n_playlists)

    return {
        'statusCode': 200,
        'body': 'Playlists enqueued for processing'
    }