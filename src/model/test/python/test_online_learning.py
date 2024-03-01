# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:25:56 2023

@author: nicol
"""
import test_utils

from common.utils import load_df_from_local_pickles
from core.clusterer import Clusterer

tests_path = test_utils.TESTS_PATH
test_name = test_utils.TEST_NAME

folder_path = f'{tests_path}/results/{test_name}'
test_utils.make_test_results_folder(folder_path)

# Load the dataset
dataset = load_df_from_local_pickles(folder_path)
# Load the configuration
config = test_utils.load_test_config()

# Calculate the midpoint of the DataFrame
midpoint = len(dataset) // 2

# Split the DataFrame into two halves
first_half = dataset.iloc[:midpoint]
second_half = dataset.iloc[midpoint:]


# Initialize and use the Clusterer
clusterer = Clusterer(config)
clusterer.partial_cluster_tracks(first_half)

clusterer = Clusterer(config, clusterer.model) # passing the first clusterer's model
clusterer.partial_cluster_tracks(second_half)