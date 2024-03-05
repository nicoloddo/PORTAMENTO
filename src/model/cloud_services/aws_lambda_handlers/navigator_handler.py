# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:03:47 2024

@author: nicol
"""

from cloud_services.aws_utilities.aws_s3_utils import read_file_from_s3
from core.birch_tree_navigator import BirchTreeNavigator

import json
import pandas as pd
import pickle

def lambda_handler(event, context):
    # TODO
    # Add url referer check
    
    model_id = event['headers'].get('model-id')
    node_id = event['headers'].get('node-id')
    
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
        # Extract the data the base model has been trained on        
        base_data_key = f'{base_model_id}/data.csv'
        base_dataset_file = read_file_from_s3(base_data_key)
        base_dataset = pd.read_csv(base_dataset_file)
        
        # Merge the two datasets to get the full database of the clusterer model
        nav_dataset = pd.concat([base_dataset, dataset]).drop_duplicates(subset='id')
        
    else: # Initialize without base model
        nav_dataset = dataset
        
    node_json = navigator.get_node(node_id).to_json(nav_dataset, columns_blacklist=["artists", "album"]) # This line gets the json
    
    return {
        'statusCode': 200,
        'body': node_json
    }