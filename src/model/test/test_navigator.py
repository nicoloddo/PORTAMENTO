# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:47 2023

@author: nicol
"""

import test_utils

import json
import pickle

from common.utils import load_df_from_local_pickles
from core.birch_tree_navigator import BirchTreeNavigator

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
        
        # Print Node information and collect input from user on the next node to navigate to
        if current_node.is_leaf: # Node is leaf, only print the songs of the node
            print("This node is a leaf node and has no further children.")
            print(f"These are its {len(current_node.samples)} songs (max 5 are displayed):")
            test_utils.print_songs(current_node.samples, dataset)
            
            # Get user input for what to do
            user_input = input("Enter '-' to go to the parent node (or enter 'exit' to quit): ") 
        
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
            if not current_node.is_leaf:
                # Update the node_id and continue
                current_node_id += user_input
            
    except Exception as e:
        print(f"An error occurred: {e}")
        break

node = current_node