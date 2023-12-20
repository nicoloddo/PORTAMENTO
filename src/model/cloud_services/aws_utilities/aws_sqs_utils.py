# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:49:16 2023

@author: nicol
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json

from common.utils import load_env_var, MAX_IDS_PER_REQUEST

FETCH_QUEUE_URL = load_env_var('FETCH_QUEUE_URL')
MERGE_QUEUE_URL = load_env_var('MERGE_QUEUE_URL')
ENDPOINT_URL = load_env_var('ENDPOINT_URL', required=False)

def enqueue_next_batch(playlist_uri, request_id, req_n_playlists, next_start_index, next_batch_size=MAX_IDS_PER_REQUEST, queue_url=FETCH_QUEUE_URL, endpoint_url=ENDPOINT_URL):
    _enqueue_fetch(playlist_uri, request_id, req_n_playlists, next_start_index, next_batch_size, queue_url, endpoint_url)

def enqueue_playlist(playlist_uri, request_id, req_n_playlists, batch_size=MAX_IDS_PER_REQUEST, queue_url=FETCH_QUEUE_URL, endpoint_url=ENDPOINT_URL):
    _enqueue_fetch(playlist_uri, request_id, req_n_playlists, 0, batch_size, queue_url, endpoint_url)
    
def _enqueue_fetch(playlist_uri, request_id, req_n_playlists, start_index, batch_size, queue_url=FETCH_QUEUE_URL, endpoint_url=ENDPOINT_URL):
    """
    Enqueues a message to an SQS queue for processing a batch of a Spotify playlist.

    :param playlist_uri: The URI of the Spotify playlist.
    :param request_id: A unique identifier for the request.
    :param start_index: The starting index for the batch in the playlist.
    :param batch_size: The size of the batch.
    :param queue_url: Optional. The URL of the SQS queue.
    :param endpoint_url: Optional. URL of the SQS service endpoint.
    :return: A response indicating the success or failure of the operation.
    """
    try:
        # Create an SQS client
        if endpoint_url:
            # Use the specified endpoint URL
            sqs = boto3.client('sqs', endpoint_url=endpoint_url)
        else:
            # Default to AWS SQS
            sqs = boto3.client('sqs')

        # Prepare the message
        message = {
            'request_id': request_id,
            'req_n_playlists': req_n_playlists,
            'playlist_uri': playlist_uri,
            'start_index': start_index,
            'batch_size': batch_size
        }

        # Send the message
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
        return {'statusCode': 200, 'body': 'Message enqueued successfully', 'response': response}

    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred while enqueuing the message: {e}")
        return {'statusCode': 500, 'body': f"Failed to enqueue message: {e}"}

def enqueue_database_merge(request_id, req_n_playlists, queue_url=MERGE_QUEUE_URL, endpoint_url=ENDPOINT_URL):
    """
    Enqueues a message to an SQS queue to trigger a database merge operation.

    :param request_id: A unique identifier for the request.
    :param queue_url: The URL of the SQS queue.
    :param endpoint_url: Optional. URL of the SQS service endpoint.
    :return: A response indicating the success or failure of the operation.
    """
    try:
        # Create an SQS client
        if endpoint_url:
            # Use the specified endpoint URL
            sqs = boto3.client('sqs', endpoint_url=endpoint_url)
        else:
            # Default to AWS SQS
            sqs = boto3.client('sqs')

        # Prepare the message
        message = {
            'request_id': request_id,
            'req_n_playlists': req_n_playlists
            }

        # Send the message
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
        return {'statusCode': 200, 'body': 'Message enqueued successfully', 'response': response}

    except (BotoCoreError, ClientError) as e:
        print(f"An error occurred while enqueuing the message: {e}")
        return {'statusCode': 500, 'body': f"Failed to enqueue message: {e}"}