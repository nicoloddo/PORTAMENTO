# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:19:03 2023

@author: nicol
"""
from common.utils import ordinal_ids_to_true_ids, dataset_select
import numpy as np
import json

class BirchTreeNavigator:
    """
    Handles navigation through the nodes of a BIRCH tree clustering model.
    """

    def __init__(self, birch_clusterer):
        """
        Initializes the BirchTreeNavigator with a clustering model.

        :param birch_clusterer: The BIRCH clustering model.
        """
        self.birch_clusterer = birch_clusterer
        self.model = birch_clusterer.model
        self._lookup = birch_clusterer.lookup

    def select_node(self, node_id):
        """
        Iteratively navigates a BIRCH tree to find and return the node specified by node_id.
        Optimizes navigation for nodes with a single subcluster and checks for leaf nodes.

        :param node_id: A string of numbers where each number represents the index of the child node to navigate to at the current level.
        :return: The BIRCH tree node specified by node_id.
        """
    
        current_node = self.model.root_
    
        for i, char_id in enumerate(node_id[1:]):  # Start from the second character as the first is always '0' for the root
            while len(current_node.subclusters_) == 1 and not current_node.is_leaf:
                # If there's only one subcluster and it's not a leaf, skip directly to its child
                current_node = current_node.subclusters_[0].child_
    
            # If the current node is a leaf, issue a warning and break the loop
            if current_node.is_leaf:
                print(f"Warning: Search of node '{node_id}' has been truncated at node '{node_id[:i+1]}': reached a leaf node.")
                break
    
            index = int(char_id)
    
            # Check if the current node has the required subcluster
            if index >= len(current_node.subclusters_):
                raise IndexError(f"Subcluster index {index} is out of range for the current node.")
    
            current_node = current_node.subclusters_[index].child_
    
        return current_node
    
    def get_node(self, node_id):
        """
        Retrieves a BirchTreeNavigatorNode for a specific node in the BIRCH tree.

        :param node_id: A string representing the path to the node.
        :return: BirchTreeNavigatorNode representing the node.
        """
        node = self.select_node(node_id)
        return BirchTreeNavigatorNode(node, node_id, self._lookup)
    
    
class BirchTreeNavigatorNode:
    """
    Represents a node in the BIRCH tree, encapsulating relevant information and functionalities.
    """

    def __init__(self, node, node_id, lookup):
        """
        Initializes the BirchTreeNavigatorNode with a node from the BIRCH tree.

        :param node: The node from the BIRCH tree.
        :param node_id: The id of the node as a string of numerical values (the ordinal ids starting from the root)
        :param lookup: The lookup table to link the sample index to basic song information.
        """
        self.node_id = node_id
        self._node = node
        self._lookup = lookup
        
        self.is_leaf = node.is_leaf
        self.samples = set()
        
        self._samples_ordinal_ids = set()
        self._children = self._get_children_info(self._node)
        
        self.n_children = len(self._children)

    def _get_children_info(self, node):
        """
        Retrieves the children information for the given node. And populates a collective self.sample
        set with all the children's samples (only unique values).
    
        :param node: The node from the BIRCH tree.
        :return: List of dictionaries, each representing a child node with its centroid and samples.
        """
        children_info = []
        for subcluster in node.subclusters_:
            if not node.is_leaf:
                child_info = {
                    'is_leaf': subcluster.child_.is_leaf,
                    'centroid': subcluster.centroid_,
                    'samples': set(subcluster.samples), # Take only unique values (if the fetching had a good filter_callback this should not be necessary)
                    'n_samples': subcluster.n_samples_,
                }
                children_info.append(child_info)
                
            self._samples_ordinal_ids.update(subcluster.samples) # Collect the samples from the child
            samples_true_ids = ordinal_ids_to_true_ids(subcluster.samples, self._lookup)
            self.samples.update(samples_true_ids)

        return children_info
    
    def get_child_samples(self, child):
        """
        Returns the samples (spotify ids) of the given child of the node.
    
        :param child: Ordinal index of the child inside the children array of the node
        :return: List of dictionaries, each representing a child node with its centroid and samples.
        """
        return ordinal_ids_to_true_ids(self._children[child]['samples'], self._lookup)
        
    def get_child_n_samples(self, child):
        return self._children[child]['n_samples']
        
    def get_child_is_leaf(self, child):
        return self._children[child]['is_leaf']
    
    def get_child_centroid(self, child):
        return self._children[child]['centroid']
    
    def to_json(self, dataset, columns_blacklist=[]):
        """
        Converts the node and its children's data into a JSON string. This includes information
        such as the node's ID, if it's a leaf, the samples associated with the node and its children,
        and the number of children nodes.
    
        The method filters the dataset's columns to exclude those specified in the columns_blacklist.
        Each node's samples are then converted into a dictionary indexed by their row indices in the dataset.
    
        :param dataset: The pandas DataFrame containing the data.
        :param columns_blacklist: List of column names to be excluded from the final JSON.
        :return: A JSON string representation of the node and its children's data.
        """
    
        # Filter the dataset columns based on the blacklist
        columns_to_select = [col for col in dataset.columns if col not in columns_blacklist]
    
        # Convert the current node's samples to a dictionary
        if self.is_leaf:
            node_samples = dataset_select(dataset, self.samples, columns_to_select).to_dict(orient='index')
        else:
            node_samples = {} # If the node is not a leaf, the samples can be retrieved from the children
        
        children_info = []
        # Iterate over the children to get their samples
        for i in range(self.n_children):
            unique_child_samples = set(self.get_child_samples(i))
            # Convert each child's samples to a dictionary
            child_samples = dataset_select(dataset, unique_child_samples).to_dict(orient='index')
            centroid = self.get_child_centroid(i)
            centroid = np.round(centroid, decimals=2).tolist()
            children_info.append({"is_leaf": self.get_child_is_leaf(i), "samples": child_samples, "centroid": centroid})
        
        # Compile the node's data into a dictionary
        data = {
            "node_id": self.node_id,
            "is_leaf": self.is_leaf,
            "samples": node_samples,
            "n_children": self.n_children,
            "children": children_info
        }
        
        # Convert the dictionary to a JSON string with indentation for readability
        return json.dumps(data, indent=4)



