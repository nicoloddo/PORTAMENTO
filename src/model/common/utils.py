# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:46:17 2023

@author: nicol
"""

import os
import pandas as pd

URI_LENGTH = 39
URI_PORTION = 17
MAX_IDS_PER_REQUEST = 100  # Maximum number of IDs per Spotify feature request

def spotify_uri_to_id(uri):
    return uri[URI_PORTION:URI_LENGTH]

def load_df_from_local_pickles(datapath):
    # List all pickle files in the folder
    pickle_files = [f for f in os.listdir(datapath) if f.endswith('.pickle')]

    # Load and concatenate all DataFrames from the pickle files
    dfs = []
    for file in pickle_files:
        file_path = os.path.join(datapath, file)
        df = pd.read_pickle(file_path)
        dfs.append(df)

    # Concatenate all DataFrames
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df