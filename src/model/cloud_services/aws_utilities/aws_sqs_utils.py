# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:49:16 2023

@author: nicol
"""

import boto3
import json

from common.utils import load_env_var, MAX_IDS_PER_REQUEST

QUEUE_URL = load_env_var('QUEUE_URL')
ENDPOINT_URL = load_env_var('ENDPOINT_URL', required=False)

def enqueue_next_batch(playlist_uri, next_start_index, next_batch_size=MAX_IDS_PER_REQUEST, queue_url=QUEUE_URL, endpoint_url=ENDPOINT_URL):
    _enqueue_fetch(playlist_uri, next_start_index, next_batch_size, queue_url, endpoint_url)

def enqueue_playlist(playlist_uri, batch_size=MAX_IDS_PER_REQUEST, queue_url=QUEUE_URL, endpoint_url=ENDPOINT_URL):
    _enqueue_fetch(playlist_uri, 0, batch_size, queue_url, endpoint_url)
    
def _enqueue_fetch(playlist_uri, start_index, batch_size, queue_url, endpoint_url):
    try:
        # Create an S3 client
        if endpoint_url:
            # Use the specified endpoint URL
            sqs = boto3.client('sqs', endpoint_url=endpoint_url)
        else:
            # Default to AWS S3
            sqs = boto3.client('sqs')

        message = {
            'playlist_uri': playlist_uri,
            'start_index': start_index,
            'batch_size': batch_size
        }
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))

    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred: {e}")