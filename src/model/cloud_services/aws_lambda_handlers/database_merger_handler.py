# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 00:03:00 2023

@author: nicol

This Lambda gets triggered everytime a playlist has finished to be fetched.
It checks if all playlists in the request have been fetched
and then merges the new fetched songs with the existing database.
"""

from cloud_services.aws_utilities.aws_s3_utils import read_file_from_s3, save_to_s3, list_folder_files_s3, delete_folder_s3

import pandas as pd
from io import StringIO

import json

LASTBATCH_LABEL = 'lastbatch'

def lambda_handler(event, context):
    request_id = event.get('RequestID')
    req_n_playlists = event.get('ReqNPlaylists')
    
    # Step 1: Initialize database
    database_df = pd.DataFrame()

    # Step 2: List and read all request_id/file.csv files
    response = list_folder_files_s3(f'{request_id}/')
    files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]
    
    # Check if request has finished
    count_processed_playlists = len([file for file in files if file.endswith(f"{LASTBATCH_LABEL}.csv")])
    if count_processed_playlists != req_n_playlists:
        return {'statusCode': 500, 'body': 'Merge aborted: waiting to finish fetching all playlists in the request.'}
        
    for file_key in files:
        file = read_file_from_s3(file_key)
        if file:
            file_df = pd.read_csv(file)
            # Step 3: Merge with the main database
            database_df = pd.concat([database_df, file_df]).drop_duplicates(subset='id')

    # Step 4: Delete the request_id/ folder
    delete_folder_s3(f'{request_id}/')
    
    # Step 5: Save the merged database
    csv_buffer = StringIO()
    database_df.to_csv(csv_buffer, index=False)
    save_to_s3(csv_buffer.getvalue().encode(), f'{request_id}/data.csv')

    # Calculate appropriate branch factor based on database size
    database_size = len(database_df)
    if database_size < 1000:
        branch_factor = 50
    elif database_size < 7000:
        branch_factor = 100
    elif database_size < 30000:
        branch_factor = 200
    elif database_size < 50000:
        branch_factor = 300
    else:
        branch_factor = 400

    # Save the clusterer configuration
    clusterer_config = {
        'branch_factor': branch_factor
    }
    json_data = json.dumps(clusterer_config)
    byte_data = json_data.encode()
    save_to_s3(data=byte_data, file_name=f'{request_id}/clusterer-config.json')

    return {'statusCode': 200, 'body': 'Request database merged!'}
