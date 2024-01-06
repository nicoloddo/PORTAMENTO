# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:19:45 2023

@author: nicol
"""

import pandas as pd
from clustering_models.birch_portamento import Birch
import pickle

class Clusterer:
    """
    Main class for clustering tracks using various algorithms.
    It orchestrates the data preprocessing, clustering, and result saving.
    Only the columns for which a weight has been specified in the config are kept and used for the clustering.
    """

    def __init__(self, config, model = None):
        """
        Initializes the Clusterer with a dataset and configuration settings.

        :param config: Configuration settings for the clustering process.
        :param model: Input dataset for clustering.
        """
        self.config = config
        # Remove keys with value 0 from the weights dictionary: filter the blacklisted columns
        self.config['weights'] = {key: value for key, value in self.config['weights'].items() if value != 0}
        
        self.preprocessor = DataPreprocessor(config)
        
        if model:
            self.model = model
        else:
            self.model = self._select_clustering_model()

    def cluster_tracks(self, dataset):
        """
        Performs clustering on the track dataset.
        """
        preprocessed_data = self.preprocessor.preprocess_data(dataset)
        self.model.cluster(preprocessed_data)
        self._save_results()
    
    def partial_cluster_tracks(self, dataset):
        """
        Performs online learning with the provided new tracks.
        """
        preprocessed_data = self.preprocessor.preprocess_data(dataset)
        self.model.partial_cluster(preprocessed_data)
        self._save_results()

    def _select_clustering_model(self):
        """
        Selects the clustering model based on configuration settings.

        :return: An instance of the selected clustering model.
        """
        if self.config['algorithm'] == 'birch':
            return BirchClusterer(self.config)
        else:
            raise ValueError(f"Unknown algorithm: {self.config['algorithm']}")

    def _save_results(self):
        """
        Saves the clustering results as per the configuration settings.
        """
        if self.config['save_results']:
            # Save model
            with open(self.config['model_path'], "wb+") as file:
                pickle.dump(self.model, file)
            
            # Save clusters and centroids if required
            # This can include saving cluster data to files or databases
            # Implement specific saving logic here
        
class DataPreprocessor:
    """
    Handles preprocessing of data for clustering, including feature selection,
    normalization, and applying weights.
    """

    def __init__(self, config):
        """
        Initializes the DataPreprocessor with configuration settings.

        :param config: Configuration settings for data preprocessing.
        """
        self.config = config

    def preprocess_data(self, data):
        """
        Performs preprocessing on the given data. Sets the 'id' as the DataFrame index.
        Applies the weights for clustering. 
        Only the columns for which a weight has been specified are kept and used for the clustering.

        :param data: The data to be preprocessed.
        :return: Preprocessed data ready for clustering, with 'id' as the index.
        """
        # Check if 'id' column is present for identifier purposes
        if 'id' not in data.columns and data.index.name != 'id':
            raise ValueError("Data must contain an 'id' column or index for identifiers.")

        # Set 'id' as the DataFrame index
        if data.index.name != 'id':
            data = data.set_index('id')
            
        # Take the columns relevant for clustering
        relevant_columns = [col for col in data.columns if col in self.config['weights']]
        data = data[relevant_columns].copy() # I do the copy to not operate on a slice of the dataset, remove the .copy() if it is heavy on memory
        
        # Normalize tempo if included in relevant columns
        if 'tempo' in data.columns:
            data['tempo'] = self.normalize_column(data['tempo'], self.config['tempo_range']['min'], self.config['tempo_range']['max'])

        # Apply weights to features
        weights_series = pd.Series(self.config['weights'])
        data = data.mul(weights_series, axis=1)
        
        return data
    
    def deweight_data(self, data):
        """
        Restores the data to the value before the application of weights. 
        The normalization procedures are not reestored by this application.
        
        :param data: The data to be preprocessed.

        :return: The data restored from the weights
        """
        weights_series = pd.Series(self.config['weights'])
        return data.mul(1/weights_series, axis=1)
        
    def normalize_column(self, column, min_value, max_value):
        """
        Normalizes a column to a range between 0 and 1.

        :param column: The pandas Series (column) to be normalized.
        :param min_value: The minimum value for normalization.
        :param max_value: The maximum value for normalization.
        :return: Normalized pandas Series.
        """
        return (column - min_value) / (max_value - min_value)
    

class BirchClusterer:
    """
    Implements clustering using the BIRCH algorithm.
    """

    def __init__(self, config):
        """
        Initializes the BirchClusterer with configuration settings.

        :param config: Configuration settings specific to the BIRCH algorithm.
        """
        self.config = config
        self.model = Birch(threshold=self.config['birch_threshold'], branching_factor=self.config['branch_factor'])
        self.lookup = {} # Dictionary containing the original ids of the songs and their ordinal index, because the birch saves them by ordinal index in the tree

    def cluster(self, data):
        """
        Performs clustering on the provided data using the BIRCH algorithm.

        :param data: Data to be clustered.
        """
        self.lookup = {sample: song_id for sample, song_id in enumerate(data.index)}
        self.model.fit(data)
        self.labels = self.model.labels_
        self.centroids = self.model.subcluster_centers_
        
    def partial_cluster(self, data):
        """
        Performs partial clustering (online learning) on the provided data using the BIRCH algorithm.

        :param data: Data to be clustered.
        """
        
        additional_lookup = {self.model.base_index_ + sample: song_id for sample, song_id in enumerate(data.index)}
        self.lookup.update(additional_lookup)
        
        self.model.partial_fit(data)
        
        self.labels = self.model.labels_
        self.centroids = self.model.subcluster_centers_

    # Additional methods for Birch specific operations can be added here

