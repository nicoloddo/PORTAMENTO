# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 17:19:45 2023

@author: nicol
"""

import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from clustering_models.birch_portamento import Birch
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

class Clusterer:
    """
    Main class for clustering tracks using various algorithms.
    It orchestrates the data preprocessing, clustering, and result saving.
    Only the columns for which a weight has been specified in the config are kept and used for the clustering.
    """

    def __init__(self, dataset, config):
        """
        Initializes the Clusterer with a dataset and configuration settings.

        :param dataset: Input dataset for clustering.
        :param config: Configuration settings for the clustering process.
        """
        self.dataset = dataset
        self.config = config
        self.preprocessor = DataPreprocessor(config)

    def cluster_tracks(self):
        """
        Performs clustering on the track dataset.
        """
        preprocessed_data = self.preprocessor.preprocess_data(self.dataset)
        self.model = self._select_clustering_model()
        self.model.cluster(preprocessed_data)
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
        if 'id' not in data.columns:
            raise ValueError("Data must contain an 'id' column for identifiers.")

        # Set 'id' as the DataFrame index
        data = data.set_index('id')

        # Filter columns based on weights keys
        relevant_columns = [col for col in data.columns if col in self.config['weights']]
        data = data[relevant_columns]
        
        # Normalize tempo if included in relevant columns
        if 'tempo' in data.columns:
            data['tempo'] = self.normalize_column(data['tempo'], self.config['tempo_range']['min'], self.config['tempo_range']['max'])

        # Apply weights to features
        if 'weights' in self.config:
            weights_series = pd.Series(self.config['weights'])
            data = data.mul(weights_series, axis=1)
        
        return data

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

    def cluster(self, data):
        """
        Performs clustering on the provided data using the BIRCH algorithm.

        :param data: Data to be clustered.
        """
        self.model.fit(data)
        self.labels = self.model.labels_
        self.centroids = self.model.subcluster_centers_

    # Additional methods for Birch specific operations can be added here

