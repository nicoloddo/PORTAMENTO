# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:49:16 2023

@author: nicol
"""

import boto3
import json

def enqueue_next_batch(playlist_uri, next_start_index, next_batch_size):
    sqs = boto3.client('sqs')
    queue_url = 'YOUR_SQS_QUEUE_URL'  # Replace with your SQS queue URL

    message = {
        'playlist_uri': playlist_uri,
        'start_index': next_start_index,
        'batch_size': next_batch_size
    }
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
