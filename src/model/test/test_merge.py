# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:48:37 2023

@author: nicol
"""

import test_utils

import pandas as pd
import os

from common.utils import load_df_from_local_pickles

tests_path = test_utils.TESTS_PATH
TEST_NAME = 'mosiselecta'

folder_path = f'{tests_path}/results/{TEST_NAME}'
test_utils.make_test_results_folder(folder_path)
    
output_csv = 'output.csv'
output_path = f'{folder_path}/{output_csv}'

# Concatenate all DataFrames
merged_df = load_df_from_local_pickles(folder_path)

# Export the merged DataFrame to a CSV file
merged_df.to_csv(output_path, index=False)