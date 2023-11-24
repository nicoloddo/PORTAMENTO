# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:46:38 2023

@author: nicol

This will be an AWS Lambda handler responsible for processing a single playlist's batch of songs.
It will be triggered by messages from the SQS queue, 
each representing a batch of songs to fetch from a Spotify playlist. 
The handler will utilize the SpotifyDataFetcher to fetch the songs and then enqueue the next batch if needed.
"""

from common.utils import spotify_uri_to_id

import json
from core.spotify_data_fetcher import SpotifyBatchDataFetcher
from aws_utilities.aws_s3_utils import save_to_s3
from aws_utilities.aws_sqs_utils import enqueue_next_batch

def lambda_handler(event, context):
    # Process each message in the SQS event
    for record in event['Records']:
        message = json.loads(record['body'])
        playlist_uri = message['playlist_uri']
        start_index = message['start_index']
        batch_size = message['batch_size']

        # Initialize the SpotifyDataFetcher
        playlist_fetcher = SpotifyBatchDataFetcher(playlist_uri, batch_size)  # Define your batch size
        playlist_fetcher.fetch_playlist()
        # Fetch songs from the playlist
        songs = playlist_fetcher.fetch_batch_from_playlist(start_index)

        # Save the fetched songs
        save_to_s3(songs, f'{spotify_uri_to_id(playlist_uri)}_{start_index}.pickle')

        # Check if there are more songs to fetch and enqueue the next batch
        total_songs = playlist_fetcher.total_songs_in_playlist()
        if start_index + batch_size < total_songs: # The playlist is not finished
            next_start_index = start_index + batch_size
            next_batch_size = batch_size # You can manipulate this to only use the remaining amount of songs for the last batch
            enqueue_next_batch(playlist_uri, next_start_index, next_batch_size)
        else: # The playlist is finished
            return {'statusCode': 200, 'body': 'Playlist processed'}

    return {'statusCode': 200, 'body': 'Batch processed'}
