# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 00:03:00 2023

@author: nicol

This Lambda gets triggered everytime a playlist has finished to be fetched.
It checks if all playlists in the request have been fetched
and then merges the new fetched songs with the existing database.
"""

from cloud_services.aws_utilities.aws_s3_utils import get_database_from_s3, read_file_from_s3, save_to_s3, list_folder_files_s3, delete_folder_s3

import pandas as pd
from io import StringIO
import json

LASTBATCH_LABEL = 'lastbatch'

def lambda_handler(event, context):
    record = event['Records'][0]
    message = json.loads(record['body'])
    request_id = message['request_id']
    req_n_playlists = message['req_n_playlists']
    
    # Step 1: Read the main database file
    database_file = get_database_from_s3()
    if database_file is None:
        print('Failed to read the main database: the file may not exist')
        database_df = pd.DataFrame()
    else:
        database_df = pd.read_csv(database_file)

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

    return {'statusCode': 200, 'body': 'Request database merged!'}
