# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 22:39:58 2023

@author: nicol
"""

directory = '../test/mosiselecta/'
import os
import pandas as pd

# Example usage
folder_path = '../test/mosiselecta'  # Replace with your folder path
output_csv = 'output.csv'            # Replace with your desired output CSV file name
output_path = os.path.join(folder_path, output_csv)

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

