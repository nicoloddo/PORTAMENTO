# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:22:47 2023

@author: nicol
"""

import test_utils

from test_utils import load_df_from_local_pickles
from core.birch_tree_navigator import BirchTreeNavigator

import pickle
import pandas as pd

tests_path = test_utils.TESTS_PATH
data_test_name = test_utils.TEST_NAME
from_pickles = test_utils.FROM_PICKLES

data_folder_path = f'{tests_path}/results/{data_test_name}'

# Load the dataset
if from_pickles:
    dataset = load_df_from_local_pickles(data_folder_path)
else:
    dataset = pd.read_csv(f'{data_folder_path}/data.csv', index_col='id')

# Load the configuration
config = test_utils.load_test_config()
    
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
            test_utils.print_songs_from_idlist(current_node.samples, dataset)
            
            # Get user input for what to do
            user_input = input("Enter '-' to go to the parent node (or enter 'exit' to quit): ") 
        
        else: # Node is not leaf, let's print its children
            print()
            print('---------------------------------------')
            print(f"Current node ID is '{current_node_id}'. These are its children and their songs:")
            for i in range(current_node.n_children):
                
                print()
                if current_node.get_child_is_leaf(i):
                    print(f"{i}: Child {i} (leaf)")
                else:
                    print(f"{i}: Child {i}")

                print(f"Centroid: {current_node.get_child_deweighted_centroid_dict(i)}")
                representative_id, n_representative_ids, distances = current_node.get_child_representative_id(i, dataset)
                print(f"Most representative ID: {representative_id}")
                print(f"Number of songs within radius: {n_representative_ids}")
                
                # And let's print the songs of each children
                print(f"With {current_node.get_child_n_samples(i)} songs, among which:")
                test_utils.print_songs_from_idlist(current_node.get_child_samples(i), dataset)

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
            if not current_node.is_leaf:
                # Update the node_id and continue
                current_node_id += user_input
            
    except Exception as e:
        print(f"An error occurred: {e}")
        break

node = current_node