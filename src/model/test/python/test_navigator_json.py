# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:32:07 2023

@author: nicol
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:47 2023

@author: nicol
"""

import test_utils

import pickle
import json
import pandas as pd

from test_utils import load_df_from_local_pickles
from core.birch_tree_navigator import BirchTreeNavigator

tests_path = test_utils.TESTS_PATH
test_name = test_utils.TEST_NAME
from_pickles = test_utils.FROM_PICKLES

folder_path = f'{tests_path}/results/{test_name}'
test_utils.make_test_results_folder(folder_path)

# Load the dataset
if from_pickles:
    dataset = load_df_from_local_pickles(folder_path)
else:
    dataset = pd.read_csv(f'{folder_path}/data.csv', index_col='id')

# Load the configuration
config = test_utils.load_test_config()
    
with open(config['model_path'], 'rb') as file:
    loaded_model = pickle.load(file)

navigator = BirchTreeNavigator(loaded_model)

# Start the navigation
current_node_id = "0"
while True:
    node_json = navigator.get_node(current_node_id).to_json(dataset, columns_blacklist=["artists", "album", "disc_number"]) # This line gets the json
    current_node = json.loads(node_json) # Transform into python dict
    
    # Print Node information and collect input from user on the next node to navigate to
    if current_node['is_leaf']: # Node is leaf, only print the songs of the node
        print("This node is a leaf node and has no further children.")
        samples = pd.DataFrame.from_dict(current_node['samples'], orient='index')
        print(f"These are its {len(samples)} songs (max 5 are displayed):")
        test_utils.print_songs_from_df(samples)
        
        # Get user input for what to do
        user_input = input("Enter '-' to go to the parent node (or enter 'exit' to quit): ") 
    
    else: # Node is not leaf, let's print its children
        print()
        print('---------------------------------------')
        print(f"Current node ID is '{current_node_id}'. These are its children and their songs:")
        for i in range(len(current_node['children'])):
            
            print()
            if current_node['children'][i]['is_leaf']:
                print(f"{i}: Child {i} (leaf)")
            else:
                print(f"{i}: Child {i}")
            
            # And let's print the songs of each children
            child_track = pd.DataFrame(current_node['children'][i]['track'])
            child_meta = pd.DataFrame(current_node['children'][i]['meta'])
            child_samples = pd.concat([child_track, child_meta], axis=1)
            print(f"With {len(child_samples)} songs, among which:")
            test_utils.print_songs_from_df(child_samples)

        # Get user input for the next node to navigate
        print()
        user_input = input("Enter the index of the next children to navigate to, or enter '-' to go to the parent node (enter 'exit' to quit): ") 
    
    # Conditionals that act on what to do given the user input
    if user_input.lower() == 'exit':
        # User said exit
        break
    elif user_input.lower() == '-': 
        # User said visit parent node: we just delete the last char of the node_id
        if len(current_node_id)>1: # But only if we are not at the root
            current_node_id = current_node_id[:-1]
        else:
            print()
            print('---------------------------------------')
            print("! You are already at the root node, there is no parent to navigate to.")
    elif user_input.isdigit(): 
        # User gave a number, we visit the following node
        if not current_node['is_leaf']:
            # Update the node_id and continue
            current_node_id += user_input

node = current_node