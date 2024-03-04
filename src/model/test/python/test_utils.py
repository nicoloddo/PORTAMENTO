# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:44:49 2023

@author: nicol
"""

from common.utils import running_in_docker, load_env_var

import os
import json
import pandas as pd

TEST_NAME = 'mosiselecta'

def load_test_config():
    with open(f'{TESTS_PATH}/clusterer_test_config.json', 'r') as file:
        config = json.load(file)
    config['model_path'] = f'{TESTS_PATH}/results/{TEST_NAME}/model.pkl'
    return config

def load_df_from_local_pickles(datapath):
    # List all pickle files in the folder and sort them by filename to keep consistency across OS. 
    # On Linux os.listdir returns a list ordered by file creation. On windows it is ordered by filename.
    # By adding sorted() we make sure both return the same array.
    pickle_files = sorted([f for f in os.listdir(datapath) if f.endswith('.pickle')])

    # Load and concatenate all DataFrames from the pickle files
    dfs = []
    for file in pickle_files:
        file_path = os.path.join(datapath, file)
        df = pd.read_pickle(file_path)
        dfs.append(df)

    # Concatenate all DataFrames
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Remove duplicates based on 'id' column
    merged_df = merged_df.drop_duplicates(subset='id')
    
    # Set the 'id' column as the index
    merged_df = merged_df.set_index('id')

    return merged_df
    
def make_test_results_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
def print_songs_from_idlist(samples, dataset, max_print = 5):
    names = ""
    for i, sample in enumerate(samples):
        names += dataset.loc[sample]['name']
        if i == len(samples) -1: # We reached the last sample, let's not add any punctuation
            break
        if i >= max_print:
            names += '...'
            break
        else: names += ', '
    print(names)
    
def print_songs_from_df(samples, max_print = 5):
    # Extract the top 5 names from the 'samples' DataFrame
    top_names = samples['name'].head(5).tolist()  # Replace 'name' with the actual column name
    
    # Check if the DataFrame has more than 5 rows
    if len(samples) > max_print:
        top_names_string = ', '.join(top_names) + ', ...'
    else:
        top_names_string = ', '.join(top_names)
    
    print(top_names_string)


#****************************************************************************
if running_in_docker():
    # If running in Docker, use the environment variable
    TESTS_PATH = load_env_var('PYTHON_TESTS_PATH')
else: # Not running in Docker, use static paths
    TESTS_PATH = '.'
    make_test_results_folder("./results")