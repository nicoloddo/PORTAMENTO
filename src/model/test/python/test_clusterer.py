# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:25:56 2023

@author: nicol
"""

import test_utils

from test_utils import load_df_from_local_pickles
from core.clusterer import Clusterer

import pickle
import pandas as pd

tests_path = test_utils.TESTS_PATH
test_name = test_utils.TEST_NAME

folder_path = f'{tests_path}/results/{test_name}'
test_utils.make_test_results_folder(folder_path)

# Load the dataset
from_pickles = False
if from_pickles:
    dataset = load_df_from_local_pickles(folder_path)
else:
    dataset = pd.read_csv(f'{folder_path}/data.csv')

# Load the configuration
config = test_utils.load_test_config()

def local_pickle_save(model, path):
    with open(path, "wb+") as file:
        pickle.dump(model, file)
        
# Initialize and use the Clusterer
clusterer = Clusterer(config, save_callback = local_pickle_save)
clusterer.cluster_tracks(dataset)
print("Done!")