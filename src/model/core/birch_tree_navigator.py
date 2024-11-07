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
    AUDIO_COLUMNS = ['acousticness', 'danceability', 'energy', 
                     'instrumentalness', 'key', 'liveness', 
                     'loudness', 'mode', 'speechiness', 'tempo', 
                     'time_signature', 'valence'] # Audio features
    TRACK_COLUMNS = AUDIO_COLUMNS + ['duration_ms', 'popularity'] # Track features (audio + numerical metadata)

    ID_COLUMN = 'id'
    META_COLUMNS = [ID_COLUMN, 
                    'album', 'album_name', 'album_id', 
                    'artist', 'artist_name', 'artists_id', 
                    'disc_number', 'name', 'playlist', 
                    'preview_url', 'track_number', 'uri'] # Metadata features

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

        weights = self.birch_clusterer.config['weights']
        return BirchTreeNavigatorNode(node, node_id, self._lookup, weights)
    
    
class BirchTreeNavigatorNode:
    """
    Represents a node in the BIRCH tree, encapsulating relevant information and functionalities.
    """

    def __init__(self, node, node_id, lookup, weights):
        """
        Initializes the BirchTreeNavigatorNode with a node from the BIRCH tree.

        :param node: The node from the BIRCH tree.
        :param node_id: The id of the node as a string of numerical values (the ordinal ids starting from the root).
        :param lookup: The lookup table to link the sample index to basic song information.
        :param weights: The weights used to cluster the data.
        """
        self.node_id = node_id
        self._node = node
        self._lookup = lookup
        self.weights = weights
        
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

    def get_child_deweighted_centroid_dict(self, child):
        centroid = self.get_child_centroid(child)

        # Convert centroid array to dictionary using weights keys
        if len(centroid) != len(self.weights):
            raise ValueError(f"Centroid length ({len(centroid)}) does not match weights length ({len(self.weights)})")
        
        # Deweight the centroid values directly using numpy array operations
        weights_array = np.array(list(self.weights.values()))
        deweighted_centroid = centroid / weights_array
        
        # Create dictionary with deweighted values
        centroid_dict = {key: np.round(value, decimals=2) 
                        for key, value in zip(self.weights.keys(), deweighted_centroid)}
        
        return centroid_dict
    
    def get_child_representative_id(self, child, dataset):
        """
        Returns the most representative song id of the child node, the number of songs within a radius
        of the centroid and the distances of all songs to the centroid sorted by distance.
        """
        # Calculate Euclidean distances from each song to the centroid
        distances = []
        RADIUS = 0.5  # Constant radius threshold
        weights = {k: v for k, v in self.weights.items() if k not in ['tempo', 'key']}

        centroid_dict = self.get_child_deweighted_centroid_dict(child)
        centroid_dict = {k: v for k, v in centroid_dict.items() if k in weights.keys()}
        centroid = np.array(list(centroid_dict.values()))
        child_track = dataset_select(dataset, self.get_child_samples(child), weights.keys())

        for idx, row in child_track.iterrows():
            # Get feature values for this song
            song_features = row.values
            
            # Calculate weighted Euclidean distance to centroid
            weights_array = np.array(list(weights.values()))
            distance = np.sqrt(np.sum(weights_array * (song_features - centroid)**2))
            distances.append((idx, distance))
        
        # Sort by distance and get songs within radius
        distances.sort(key=lambda x: x[1])
        representative_ids = [idx for idx, dist in distances if dist <= RADIUS]
        
        # Get the most popular song among the representative songs
        popularity_df = dataset_select(dataset, self.get_child_samples(child), ['popularity'])
        if representative_ids:
            representative_tracks = popularity_df.loc[representative_ids]
            most_representative_id = representative_tracks.loc[representative_tracks['popularity'].idxmax()].name
        else:
            # Fallback to most popular in cluster if no songs within radius
            most_representative_id = popularity_df.loc[popularity_df['popularity'].idxmax()].name

        return most_representative_id, len(representative_ids), distances
    
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
        track_columns_to_select = [col for col in dataset.columns if col in BirchTreeNavigator.TRACK_COLUMNS and col not in columns_blacklist]
        meta_columns_to_select = [col for col in dataset.columns if col in BirchTreeNavigator.META_COLUMNS and col not in columns_blacklist]
    
        # The node's samples are not included in the JSON because they can be retrieved from the children.
        # Make sure to not allow entering a node with no children (leaf nodes)
        
        children_info = []
        # Iterate over the children to get their samples
        for i in range(self.n_children):
            centroid_dict = self.get_child_deweighted_centroid_dict(i)

            # Get the unique samples of the child
            unique_child_samples = set(self.get_child_samples(i))

            most_representative_id, n_representative_ids, distances = self.get_child_representative_id(i, dataset)

            # Create a dictionary of distances for quick lookup, converting to float and rounding
            distance_dict = {idx: round(float(dist), 3) for idx, dist in distances}

            # Get child track data
            child_track = dataset_select(dataset, unique_child_samples, track_columns_to_select)
            # Convert to list of dictionaries, including the ID and distance for each row
            child_track = [
                {**row.to_dict(), 'distance': distance_dict[idx]} 
                for idx, row in child_track.iterrows()
            ]
            
            # Get child metadata
            child_meta = dataset_select(dataset, unique_child_samples, meta_columns_to_select)
            # Convert to list of dictionaries, including the ID for each row
            child_meta = [{'id': idx, **row.to_dict()} for idx, row in child_meta.iterrows()]

            children_info.append({
                "is_leaf": self.get_child_is_leaf(i), 
                "track": child_track, 
                "meta": child_meta, 
                "centroid": centroid_dict, 
                "most_representative_id": most_representative_id})
        
        # Compile the node's data into a dictionary
        data = {
            "node_id": self.node_id,
            "is_leaf": self.is_leaf,
            "children": children_info
        }
        
        # Convert the dictionary to a JSON string with indentation for readability
        return json.dumps(data, indent=4)



