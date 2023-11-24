# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:49:16 2023

@author: nicol
"""

import boto3
import json
from common.utils import MAX_IDS_PER_REQUEST

QUEUE_URL = 'YOUR_SQS_QUEUE_URL'  # Replace with your SQS queue URL

def enqueue_next_batch(playlist_uri, next_start_index, next_batch_size=MAX_IDS_PER_REQUEST, queue_url=QUEUE_URL):
    _enqueue_fetch(playlist_uri, next_start_index, next_batch_size)

def enqueue_playlist(playlist_uri, batch_size=MAX_IDS_PER_REQUEST, queue_url=QUEUE_URL):
    _enqueue_fetch(playlist_uri, 0, batch_size)
    
def _enqueue_fetch(playlist_uri, start_index, batch_size, queue_url):
    sqs = boto3.client('sqs')

    message = {
        'playlist_uri': playlist_uri,
        'start_index': start_index,
        'batch_size': batch_size
    }
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))