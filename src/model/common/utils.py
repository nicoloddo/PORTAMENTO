# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:46:17 2023

@author: nicol
"""

import os
import pandas as pd

import uuid
import time
import re

URI_LENGTH = 39
URI_PORTION = 17
MAX_IDS_PER_REQUEST = 100  # Maximum number of IDs per Spotify feature request

def generate_unique_request_code():
    # Create a UUID
    unique_id = uuid.uuid4()

    # Get the current timestamp
    timestamp = int(time.time())

    # Combine them to form the request code
    request_code = f"{unique_id}-{timestamp}"
    return request_code

def is_valid_spotify_playlist_uri(uri):
    """
    Validates if the given string is a valid Spotify playlist URI.

    A valid Spotify playlist URI follows the format: spotify:playlist:playlist_id
    where 'playlist_id' is exactly 22 alphanumeric characters.

    Args:
    uri (str): The Spotify playlist URI to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    # Regular expression for matching Spotify playlist URIs with exactly 22 alphanumeric characters for the ID
    pattern = r'^spotify:playlist:[0-9a-zA-Z]{22}$'
    
    # Use regex to validate the URI
    return bool(re.match(pattern, uri))

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
    
    # Remove duplicates based on 'id' column
    merged_df = merged_df.drop_duplicates(subset='id')
    
    # Set the 'id' column as the index
    merged_df = merged_df.set_index('id')

    return merged_df

def ordinal_ids_to_true_ids(ordinal_ids, lookup_table):
    """ 
    Transforms a list of ordinal ids into the true Spotify ids from a dictionary of ordinal_ids mapped to Spotify ids
    """
    return [lookup_table[ordinal_id] for ordinal_id in ordinal_ids]

def dataset_select(dataset, rows, columns = []):
    if len(columns) > 0:
        return dataset.loc[rows, columns]
    else:
        return dataset.loc[rows]

def running_in_docker():
    """Check if running in a Docker container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return 'docker' in ifh.read()
    except Exception:
        return False
    
def load_env_var(name, required=True):
    """
    Loads an environment variable. If the variable is required and not set, raises an error.
    
    :param name: The name of the environment variable.
    :param required: Boolean indicating whether the variable is required. Defaults to True.
    :return: The value of the environment variable or None if it's optional and not set.
    """
    var = os.getenv(name)
    if var is None and required:
        raise EnvironmentError(f"{name} environment variable is not set.")
    return var
    
    
# If not in Docker, load the .env file, if running in Docker, the environment variables are set in the os.
if not running_in_docker():
    from dotenv import load_dotenv
    load_dotenv()