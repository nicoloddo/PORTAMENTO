# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:03:47 2024

@author: nicol
"""

from cloud_services.aws_utilities.aws_s3_utils import (
    read_file_from_s3, 
    save_to_s3, 
    list_folder_files_s3,
    generate_presigned_url
)
from core.birch_tree_navigator import BirchTreeNavigator

import json
import pandas as pd
import pickle
from datetime import datetime, timedelta
import time

EXPIRATION_MINUTES = 1200 # 20 hours

cors_headers = {
    'Access-Control-Allow-Headers': 'Content-Type, model-id, node-id, x-api-key',
    'Access-Control-Allow-Origin': 'https://nicoloddo.github.io',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}

def generate_response(response_key, expiration_time):
    """
    Generate a standardized response with a pre-signed URL.
    
    Args:
        response_key (str): The S3 key for the response file
        expiration_time (datetime): When the response should expire
    
    Returns:
        dict: API Gateway response with pre-signed URL and expiration
    """
    presigned_url = generate_presigned_url(
        response_key,
        expiration=EXPIRATION_MINUTES * 60  # Convert minutes to seconds
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps({
            'url': presigned_url,
            'expires_at': int(expiration_time.timestamp())
        })
    }

def lambda_handler(event, context):
    print(event)
    if event['httpMethod'] == 'OPTIONS':
        # Return response for OPTIONS preflight request
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    model_id = event['headers'].get('model-id')
    node_id = event['headers'].get('node-id')
    
    print(f"Navigator starting for model {model_id}, at node {node_id}")
    
    response_key = f'{model_id}/responses/{node_id}_response.json'

    # Check for existing response
    existing_responses = list_folder_files_s3(response_key)
    
    if 'Contents' in existing_responses and existing_responses['Contents']:
        response_obj = existing_responses['Contents'][0]
        last_modified = response_obj['LastModified']
        
        # Check if the response is still valid (less than 50 minutes old)
        time_since_modified = datetime.now(last_modified.tzinfo) - last_modified
        if time_since_modified < timedelta(minutes=EXPIRATION_MINUTES - 10):
            print(f"Using cached response: {response_key}")
            expiration_time = last_modified + timedelta(minutes=EXPIRATION_MINUTES)
            return generate_response(response_key, expiration_time)
    
    # If no valid cached response exists, generate new one
    # Extract data
    data_key = f'{model_id}/data.csv'
    dataset_file = read_file_from_s3(data_key)
    dataset = pd.read_csv(dataset_file)
    
    # Extract model
    model_key = f'{model_id}/model.pkl'
    model_file = read_file_from_s3(model_key)
    model = pickle.load(model_file)
    
    # Instantiate Navigator
    navigator = BirchTreeNavigator(model)
    
    navigator_config_key = f'{model_id}/navigator-config.json'
    navigator_config_file = read_file_from_s3(navigator_config_key)
    navigator_config = json.loads(navigator_config_file)
    base_model_id = navigator_config['base-model-id']
    
    if base_model_id is not None: # Extract base data    
        print(f"Base model has been specified: {base_model_id}")    
        # Extract the data the base model has been trained on        
        base_data_key = f'{base_model_id}/data.csv'
        base_dataset_file = read_file_from_s3(base_data_key)
        base_dataset = pd.read_csv(base_dataset_file)
        
        # Merge the two datasets to get the full database of the clusterer model
        nav_dataset = pd.concat([base_dataset, dataset]).drop_duplicates(subset='id')
        
    else: # Initialize without base model
        nav_dataset = dataset
        
    nav_dataset = nav_dataset.set_index('id')
    
    # Generate node data
    node_json = navigator.get_node(node_id).to_json(
        nav_dataset, 
        columns_blacklist=["artists", "album", "disc_number"]
    )
    
    # Save response to S3 (will overwrite if exists)
    save_to_s3(
        data=node_json.encode(),
        file_name=response_key
    )
    
    # Generate response for new data
    expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_MINUTES)
    return generate_response(response_key, expiration_time)