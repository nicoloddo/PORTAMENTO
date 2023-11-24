# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:44:49 2023

@author: nicol
"""

import os
import json
from common.utils import running_in_docker, load_env_var

TEST_NAME = 'mosiselecta'

def load_test_config():
    with open(f'{TESTS_PATH}/clusterer_test_config.json', 'r') as file:
        config = json.load(file)
    config['model_path'] = f'{TESTS_PATH}/results/{TEST_NAME}/model.pkl'
    return config
    
def make_test_results_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
def print_songs(samples, dataset):
    names = ""
    for i, sample in enumerate(samples):
        names += dataset.iloc[sample]['name']
        if i == len(samples) -1: # We reached the last sample, let's not add any punctuation
            break
        if i >= 5:
            names += '...'
            break
        else: names += ', '
    print(names)

#****************************************************************************
if running_in_docker():
    # If running in Docker, use the environment variable
    TESTS_PATH = load_env_var('TESTS_PATH')
else: # Not running in Docker, use static paths
    TESTS_PATH = './'
    make_test_results_folder("./results")