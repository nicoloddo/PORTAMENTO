# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:44:49 2023

@author: nicol
"""

import os

def running_in_docker():
    """Check if running in a Docker container."""
    try:
        with open('/proc/1/cgroup', 'rt') as ifh:
            return 'docker' in ifh.read()
    except Exception:
        return False

def make_test_results_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
def print_songs(samples, dataset):
    names = ""
    for i, sample in enumerate(samples):
        names += dataset.iloc[sample]['name']
        if i == len(samples) -1: # We reached the last sample, let's not add any punctuation
            break
        if i >= 5:
            names += '...'
            break
        else: names += ', '
    print(names)
    
if running_in_docker():
    # If running in Docker, use the environment variable
    TESTS_PATH = os.getenv('TESTS_PATH')
    if TESTS_PATH is None:
        raise EnvironmentError("TESTS_PATH environment variable is not set.")
else:
    # If not in Docker, load from .env file
    from dotenv import load_dotenv
    load_dotenv()
    TESTS_PATH = './'