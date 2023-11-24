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
    return merged_df

def running_in_docker():
    """Check if running in a Docker container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return 'docker' in ifh.read()
    except Exception:
        return False
    
def load_env_var(name):
    var = os.getenv(name)
    if var is None:
        raise EnvironmentError(f"{var} environment variable is not set.")
    else: return var
    
    
# If not in Docker, load the .env file, if running in Docker, the environment variables are set in the os.
if not running_in_docker():
    from dotenv import load_dotenv
    load_dotenv()