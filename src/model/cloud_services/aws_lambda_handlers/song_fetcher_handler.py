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

from core.spotify_data_fetcher import SpotifyBatchDataFetcher
from cloud_services.aws_utilities.aws_s3_utils import save_to_s3

LASTBATCH_LABEL = 'lastbatch'

def lambda_handler(event, context):
    request_id = event['RequestID']
    playlist_uri = event['PlaylistURI']
    batch_size = event['BatchSize']
    start_index = event['StartIndex']

    # Initialize the SpotifyDataFetcher
    playlist_fetcher = SpotifyBatchDataFetcher(playlist_uri, batch_size)  # Define your batch size
    playlist_fetcher.fetch_playlist()
    # Fetch songs from the playlist
    songs = playlist_fetcher.fetch_batch_from_playlist(start_index)
    # Convert to csv file (bytes)
    csv_string = songs.to_csv(index=False)
    csv_bytes = csv_string.encode()

    # Check if there are more songs to fetch
    total_songs = playlist_fetcher.total_songs_in_playlist() # Get the total number of songs in the playlist
    if start_index + batch_size < total_songs: # The playlist is not finished
        # Save the fetched songs
        save_to_s3(csv_bytes, f'{request_id}/{spotify_uri_to_id(playlist_uri)}_{start_index}.csv')
        
        # Compute the next start_index
        next_start_index = start_index + batch_size

        # Return structure for continuation
        return {
            "continueProcessing": True,
            "nextStartIndex": next_start_index
        }

    else: # The playlist is finished
        # Save batch as last batch
        save_to_s3(csv_bytes, f'{request_id}/{spotify_uri_to_id(playlist_uri)}_{LASTBATCH_LABEL}.csv')

        # Return structure for completion
        return {
            "continueProcessing": False
        }
