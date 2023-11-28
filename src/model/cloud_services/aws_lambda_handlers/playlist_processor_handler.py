# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:43:39 2023

@author: nicol

This script will serve as the AWS Lambda handler
that initiates the process of fetching songs from Spotify playlists.
This handler will be triggered by an S3 event when a .txt file containing playlist URIs is uploaded. 
It will read these URIs and enqueue tasks in an SQS queue to process each playlist sequentially.
"""

from cloud_services.aws_utilities.aws_s3_utils import read_file_from_s3
from cloud_services.aws_utilities.aws_sqs_utils import enqueue_playlist

def lambda_handler(event, context):
    # Extract bucket name and file key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read the playlist file from S3
    playlist_uris = read_file_from_s3(bucket, key).split('\n')    

    # Iterate over playlist URIs and send messages to SQS queue
    for uri in playlist_uris:
        enqueue_playlist(uri)

    return {
        'statusCode': 200,
        'body': 'Playlists enqueued for processing'
    }