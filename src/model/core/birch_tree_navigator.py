# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 18:19:03 2023

@author: nicol
"""

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
        self.lookup = birch_clusterer.lookup

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
        return BirchTreeNavigatorNode(node, self.lookup)
    
    
class BirchTreeNavigatorNode:
    """
    Represents a node in the BIRCH tree, encapsulating relevant information and functionalities.
    """

    def __init__(self, node, lookup):
        """
        Initializes the BirchTreeNavigatorNode with a node from the BIRCH tree.

        :param node: The node from the BIRCH tree.
        :param lookup: The lookup table to link the sample index to basic song information.
        """
        self.node = node
        self.lookup = lookup
        self.is_leaf = node.is_leaf
        self.samples = set()
        
        self._samples_ordinal_ids = set()
        self._children = self._get_children_info(node)
        
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
            samples_true_ids = self.ordinal_ids_to_true_ids(subcluster.samples)
            self.samples.update(samples_true_ids)

        return children_info
    
    def get_child_samples(self, child):
        """
        Returns the samples (spotify ids) of the given child of the node.
    
        :param child: Ordinal index of the child inside the children array of the node
        :return: List of dictionaries, each representing a child node with its centroid and samples.
        """
        return self.ordinal_ids_to_true_ids(self._children[child]['samples'])
        
    def get_child_n_samples(self, child):
        return self._children[child]['n_samples']
        
    def get_child_is_leaf(self, child):
        return self._children[child]['is_leaf']
        
    
    def ordinal_ids_to_true_ids(self, ordinal_ids):
        """ 
        Transforms a list of ordinal ids into the true spotify ids
        """
        return [self.lookup[index] for index in ordinal_ids]


