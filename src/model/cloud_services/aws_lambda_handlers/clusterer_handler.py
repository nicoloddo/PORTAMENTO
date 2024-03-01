# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:43:39 2023

@author: nicol

This script will serve as the AWS Lambda handler
that starts the clustering of the songs.
This handler will be triggered by an API Gateway event.
It will read the clusterer config in the body of the request
and start the clustering.
"""

from cloud_services.aws_utilities.aws_s3_utils import get_database_from_s3, read_file_from_s3, save_to_s3
import json
import pickle
from core.clusterer import Clusterer

def save_model_callback(model, path):
    # Serialize the model to bytes
    model_bytes = pickle.dumps(model)

    # Use save_to_s3 to save the model bytes to the specified path
    save_to_s3(model_bytes, path)

def lambda_handler(event, context):
    data_id = event['headers'].get('data-id')
    
    # Parse the config from the request body
    try:
        config = json.loads(event['body'])
    except json.JSONDecodeError:
        # Handle the case where the body is not valid JSON
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
        config['model_path'] = f'{data_id}/model.pkl'

    data_key = f'{data_id}/data.csv'
    dataset = read_file_from_s3(data_key)
    
    # Initialize and use the Clusterer
    clusterer = Clusterer(config)
    clusterer.cluster_tracks(dataset)

    return {
        'statusCode': 200,
        'body': 'Songs clustered and model saved.'
    }