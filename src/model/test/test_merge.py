# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:48:37 2023

@author: nicol
"""

import pandas as pd
import os

import test_utils

tests_path = test_utils.TESTS_PATH
TEST_NAME = 'mosiselecta'

folder_path = f'{tests_path}/results/{TEST_NAME}'
test_utils.make_test_results_folder(folder_path)
    
output_csv = 'output.csv'
output_path = f'{folder_path}/{output_csv}'

# List all pickle files in the folder
pickle_files = [f for f in os.listdir(folder_path) if f.endswith('.pickle')]

# Load and concatenate all DataFrames from the pickle files
dfs = []
for file in pickle_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_pickle(file_path)
    dfs.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(dfs, ignore_index=True)

# Export the merged DataFrame to a CSV file
merged_df.to_csv(output_path, index=False)