# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:47 2023

@author: nicol
"""

import json
import pickle

from common.utils import load_df_from_local_pickles
from core.birch_tree_navigator import BirchTreeNavigator

import test_utils

tests_path = test_utils.TESTS_PATH
TEST_NAME = 'mosiselecta'

folder_path = f'{tests_path}/results/{TEST_NAME}'
test_utils.make_test_results_folder(folder_path)

# Load the dataset
dataset = load_df_from_local_pickles(folder_path)
# Load the configuration
with open('clusterer_test_config.json', 'r') as file:
    config = json.load(file)
    
with open(config['model_path'], 'rb') as file:
    loaded_model = pickle.load(file)

navigator = BirchTreeNavigator(loaded_model)

# Start the navigation
current_node_id = "0"
while True:
    try:
        current_node = navigator.get_node(current_node_id)
        if current_node.is_leaf:
            print("This node is a leaf node and has no further children.")
            print("These are its songs:")
            test_utils.print_songs(current_node.samples, dataset)
            break
        
        else: # Node is not leaf, let's print its children
            print()
            print('---------------------------------------')
            print(f"Current node ID is '{current_node_id}'. These are its children and their songs:")
            for i, child in enumerate(current_node.children):
                
                print()
                if child['is_leaf']:
                    print(f"{i}: Child {i} (leaf)")
                else:
                    print(f"{i}: Child {i}")
                
                # And let's print the songs of each children
                print(f"With {child['n_samples']} songs, among which:")
                test_utils.print_songs(child['samples'], dataset)

        # Get user input for the next node to navigate
        user_input = input("Enter the index of the next children to navigate to (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        # Update the node_id and continue
        current_node_id += user_input
    except Exception as e:
        print(f"An error occurred: {e}")
        break

node = current_node