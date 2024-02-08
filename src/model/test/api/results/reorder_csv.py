# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:09:56 2024

@author: nicol
"""

import pandas as pd

# Load the CSV file
df = pd.read_csv('data.csv')

# Move the 'id' column to the first position
col_order = ['id'] + [col for col in df.columns if col != 'id']
df = df[col_order]

# Save the modified DataFrame back to a CSV file
df.to_csv('ordered_data.csv', index=False)

''' I am not sure why, but the AWS execution puts id in the middle of the csv rather than first.
To compare the results of the local test fetch and of the AWS cloud fetch, we need to reorder the columns.'''
