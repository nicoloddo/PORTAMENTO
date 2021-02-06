# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:00:15 2021

@author: nicol
"""
import paths_info

import pandas as pd
import numpy as np

import pickle

# IMPORT PER IL PREDICT
from sklearn.utils import check_array
from sklearn.utils.extmath import safe_sparse_dot, row_norms

class Clusters_interface:
    
    def __init__(self, user):
        
        last_path = paths_info.Path(user).last_path

        paths = pd.read_csv(last_path)
        
        with open(paths.clusterer_dump[0], "rb") as file:
            self.clusterer = pickle.load(file)
        
        # PREPROCESSING DEI DATI
        track = self.clusterer.dataset['track']
        audio = track[self.clusterer.audio_relevant_columns]  # filtro le colonne
        self.clusterer.filter_weights()   # filtro le stesse colonne dai weights
        audio = self.clusterer.format_dataset(audio)    # formatto (per ora normalizzazione dei bpm e applicazione weights)
        data_array = audio.to_numpy()    # linearizzo perchè serve alla funzione di clusterizzazione
        
        self.labels = self.node_predict(self.clusterer.model.root_, data_array)
        
        
        
        
    def node_predict(self, node, X):
        """
        Predict data using the ``centroids_`` of subclusters.

        Avoid computation of the row norms of X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data.

        Returns
        -------
        labels : ndarray, shape(n_samples)
            Labelled data.
        """
        
        # Preprocessing
        subcluster_norms = row_norms(node.centroids_, squared=True)
        
        # Sto usando questi subcluster_labels perchè non essendo il clustering finale, non serve a nulla fare la clusterizzazione dei centroidi.
        # La clusterizzazione dei centroidi veniva fatta tramite Agglomerative Clustering ed era un passaggio di clusterizzazione finale.
        # Era però utile solo nel caso in cui avessimo dichiarato di volere meno clusters di quelli formati (pari al numero di centroidi), possibile
        # specificandolo nella dichiarazione del modello durante il clustering. È in ogni caso inutile durante l'assegnamento dei label per ogni nodo.
        self.subcluster_labels_ = np.arange(len(node.centroids_))
        
        X = check_array(X, accept_sparse='csr')
        reduced_distance = safe_sparse_dot(X, node.centroids_.T)
        reduced_distance *= -2
        reduced_distance += subcluster_norms
        return self.subcluster_labels_[np.argmin(reduced_distance, axis=1)]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        