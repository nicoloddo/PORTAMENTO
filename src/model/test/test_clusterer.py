# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:25:56 2023

@author: nicol
"""

import test_utils

import json

from common.utils import load_df_from_local_pickles
from core.clusterer import Clusterer

tests_path = test_utils.TESTS_PATH
TEST_NAME = 'mosiselecta'

folder_path = f'{tests_path}/results/{TEST_NAME}'
test_utils.make_test_results_folder(folder_path)

# Load the dataset
dataset = load_df_from_local_pickles(folder_path)
# Load the configuration
with open('clusterer_test_config.json', 'r') as file:
    config = json.load(file)
    
# Initialize and use the Clusterer
clusterer = Clusterer(dataset, config)
clusterer.cluster_tracks()