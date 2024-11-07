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

from cloud_services.aws_utilities.aws_s3_utils import read_file_from_s3, save_to_s3
from core.clusterer import Clusterer

import json
import pickle
import pandas as pd

import sys
sys.setrecursionlimit(10000) # Increase recursion limit to avoid pickling errors

def save_model_callback(model, path):
    # Serialize the model to bytes
    model_bytes = pickle.dumps(model)

    # Use save_to_s3 to save the model bytes to the specified path
    save_to_s3(model_bytes, path)

def lambda_handler(event, context):
    # TODO
    # Add url referer check
    
    data_id = event['headers'].get('data-id')
    base_model_id = event['headers'].get('base-model-id')
    
    # Parse the config from the request body
    try:
        config = json.loads(event['body'])
    except json.JSONDecodeError:
        # Handle the case where the body is not valid JSON
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    
    def load_param_from_s3(config, param_name):
        try:
            clusterer_config_file = read_file_from_s3(f'{data_id}/clusterer-config.json')
            clusterer_config = json.loads(clusterer_config_file)
            config[param_name] = clusterer_config[param_name]
            return config
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Failed to load clusterer config: {str(e)}'})
            }
    
    # Only load and set the parameter if it's not already specified in config
    for param_name in ['branch_factor', 'birch_threshold']:
        if param_name not in config:
            config = load_param_from_s3(config, param_name)

    config['model_path'] = f'{data_id}/model.pkl'

    data_key = f'{data_id}/data.csv'
    dataset_file = read_file_from_s3(data_key)
    dataset = pd.read_csv(dataset_file)
    
    if base_model_id is not None: # Initialize with a base model from file
        # Extract model
        base_model_key = f'{base_model_id}/model.pkl'
        base_model_file = read_file_from_s3(base_model_key)
        base_model = pickle.load(base_model_file)
        
        clusterer = Clusterer(config, base_model, save_callback = save_model_callback)
        
    else: # Initialize without base model
        clusterer = Clusterer(config, save_callback = save_model_callback)
    
    # Use the Clusterer (it will be saved automatically)
    clusterer.partial_cluster_tracks(dataset)

    # Save the base-model to use for a navigation
    navigator_config = {'base-model-id': base_model_id}
    json_data = json.dumps(navigator_config)  # Serialize dict to a JSON formatted str
    byte_data = json_data.encode()   # Convert the JSON string to bytes
    save_to_s3(data=byte_data, file_name=f'{data_id}/navigator-config.json')

    # TODO: The clusterer should delete the previous response files since after
    # clustering we have a new model and the cached responses don't reflect it.
    
    return {
        'statusCode': 200,
        'body': 'Songs clustered and model saved.'
    }