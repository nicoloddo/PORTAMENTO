# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:00:15 2021

@author: nicol
"""

import sys

import paths_info
import datasets_utils as dt
from clustering import TRACK_AUDIO_COLUMNS, TRACK_META_NUMERICAL_COLUMNS, TRACK_META_TEXTUAL_COLUMNS, tempo_range, WEIGHT_MAX

import pandas as pd
import numpy as np

import pickle

# IMPORT PER IL PREDICT
from sklearn.utils import check_array
from sklearn.utils.extmath import safe_sparse_dot, row_norms

def main(node_id, user = 'nic'):
    '''
    QUESTO SCRIPT SERVE A RESTITUIRE ALL'INTERFACCIA I CLUSTER DEL NODO IN CUI CI TROVIAMO. AVVIA PRIMA START_TRIP SE HAI CAMBIATO DATASET O RADARS
    '''
    root = r'D:\PROJECTS\PORTAMENTO'
    paths = paths_info.Path(user, root)
    
    paths.load_pack(pd.read_csv(paths.last_path))
    
    is_radar = True
    new_radar = False
    radar = dt.Dataset(paths, is_radar, new_radar)
        
    with open(paths.clusterer_dump, "rb") as file:
        clusterer = pickle.load(file)
        
    # ASSEGNAMENTI UTILI
    model = clusterer.model
    track = clusterer.dataset['original_track']
    normalize_column(track, tempo_range['min'], tempo_range['max'], 'tempo')
    radar_df = radar.dataset['track']
    data_track = track[TRACK_AUDIO_COLUMNS + TRACK_META_NUMERICAL_COLUMNS]   # separo le informazioni numeriche
    data_meta = track[TRACK_META_TEXTUAL_COLUMNS]  # separo le informazioni testuali
    data = [data_track, data_meta]
    
    # CALCOLO IL NODO E RESTITUISCO I CLUSTER SALVANDOLO
    current_node = get_node(model.root_, node_id)
    return_clusters(current_node, data, clusterer.audio_relevant_columns, paths, 'track')
    
    # CALCOLO I LABEL DEL RADAR
    # TODO: POTREBBE CAPITARE CHE UNA CANZONE GIA' PRESENTE IN UN CLUSTER SIA ASSEGNATA IN UN PREDICT A UN CLUSTER DIVERSO.
    #       PER CUI, CONVIENE CERCARE CANZONI APPARTENENTI AL RADAR GIA' PRESENTI NEI CLUSTER E METTERE QUEL CLUSTER COME LABEL.
    radar_labels = predict_labels(radar.dataset['track'], clusterer, current_node)
    radar_df['label'] = radar_labels
    radar_track = radar_df[TRACK_AUDIO_COLUMNS + TRACK_META_NUMERICAL_COLUMNS + ['label']]   # separo le informazioni numeriche
    radar_meta = radar_df[TRACK_META_TEXTUAL_COLUMNS]  # separo le informazioni testuali
    
    # RESTITUISCO IL RADAR SALVANDOLO
    with open(paths.track_clust + r'\radar_track' + ".csv", "w+"):
            # salvo il dataset delle informazioni audio
            export_csv = radar_track.to_csv (paths.track_clust + r'\radar_track' + ".csv", index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando la parte track del radar")
    
    with open(paths.track_clust + r'\radar_meta' + ".csv", "w+"):
            # salvo il dataset delle informazioni audio
            export_csv = radar_meta.to_csv (paths.track_clust + r'\radar_meta' + ".csv", index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando la parte meta del radar")
    
    print("node_id: " + node_id) # Informazione mandata al debugging nell'interfaccia
    
    return 0


def get_node(node, node_id, iter_index = 1):
    '''
    Questa funzione viene fatta partire con node=root.
    Il node_id è una stringa composta da numeri. 
    Ognuno di questi numeri indica quale nodo seguire. Il primo numero sarà l'indice del nodo da seguire dopo il precedente e così via.
    Il root è descritto dal primo numero ed è sempre pari a 0, quindi il node_id del root è semplicemente '0'.
    Se il node_id è formato da un solo carattere, ossia siamo al root, poichè l'iter_index parte da 1, la funzione restituirà direttemente il root.
    O comunque restituirà il primo nodo root a cui non segue un solo nodo identico.
    '''
    if len(node.subclusters_) == 1: # Se ha un solo subcluster, il nodo successivo è identico, dunque saltiamo direttamente al successivo
        next_node = node.subclusters_[0].child_
        return get_node(next_node, node_id, iter_index)
    
    if iter_index < len(node_id):
        char_id = int(node_id[iter_index])
        next_node = node.subclusters_[char_id].child_
        iter_index = iter_index + 1
        return get_node(next_node, node_id, iter_index)
    else:
        return node


def predict_labels(track, clusterer, node):
    # PREPROCESSING
    audio = track[clusterer.audio_relevant_columns]  # filtro le colonne
    clusterer.filter_weights()   # filtro le stesse colonne dai weights
    audio = clusterer.format_dataset(audio)    # formatto (per ora normalizzazione dei bpm e applicazione weights)
    data_array = audio.to_numpy()    # linearizzo perchè serve alla funzione di clusterizzazione
    
    # PREDICT
    labels = node_predict(node, data_array)
    
    return labels
    
def node_predict(node, X):
    
    """
    Predict data using the ``centroids_`` of subclusters
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
    subcluster_labels_ = np.arange(len(node.centroids_))
        
    X = check_array(X, accept_sparse='csr')
    reduced_distance = safe_sparse_dot(X, node.centroids_.T)
    reduced_distance *= -2
    reduced_distance += subcluster_norms
    return subcluster_labels_[np.argmin(reduced_distance, axis=1)]



def return_clusters(node, data, columns, paths, scope):
    # Cancello il precedente return
    paths.delete_saved_clusters(paths.track_clust)
    
    # Salvo i centroidi
    centroids_df = pd.DataFrame(data = node.centroids_, columns = columns)/WEIGHT_MAX
    # SE IL NODO E' FOGLIA, I SUBCLUSTERS NON HANNO CHILD E NON POSSONO RIESEGUIRE QUESTO SCRIPT! POTREI AL LIMITE FAR NAVIGARE TRA LE CANZONI DEL CLUSTER
    centroids_df['is_leaf'] = [int(node.is_leaf)] * len(node.centroids_)    # Per cui mi segno se è un nodo foglia
    with open(paths.centroids, "w+"):
        export_csv = centroids_df.to_csv (paths.centroids, index = None, header=True)    # Esporto i centroidi
        if str(export_csv) != 'None':
            print("Errore salvando i centroidi.")
                
    for i, subcluster in enumerate(node.subclusters_):
        cluster_track = []    # cluster ausiliario usato per salvare il subcluster selezionato
        cluster_meta = []    # cluster ausiliario usato per salvare il subcluster selezionato
        cluster_track = data[0].iloc[subcluster.samples, :]  # seleziono le canzoni del dataframe track
        cluster_meta = data[1].iloc[subcluster.samples, :]  # seleziono le canzoni del dataframe meta

        with open(paths.__dict__[scope + '_clust'] + r'\track' + str(i) + ".csv", "w+"):
            # salvo il dataset delle informazioni audio
            export_csv = cluster_track.to_csv (paths.__dict__[scope + '_clust'] + r'\track' + str(i) + ".csv", index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando la parte track dei clusters")
                
        with open(paths.__dict__[scope + '_clust'] + r'\meta' + str(i) + ".csv", "w+"):
            # salvo il dataset delle informazioni audio
            export_csv = cluster_meta.to_csv (paths.__dict__[scope + '_clust'] + r'\meta' + str(i) + ".csv", index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando la parte meta dei clusters")
        
      
def normalize_column(dataframe, min_value, max_value, column):  # porto tutti gli elementi della colonna a variare tra [0, 1]
        
        for row in range(len(dataframe.index)):  #len con quell'argomento restituisce il numero di righe
            trasla = dataframe.at[row, column] - min_value    # porto la scala ad avere 0 come minimo
            normalized = trasla / (max_value - min_value)
            dataframe.at[row, column] = normalized

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])
    #main("0")     # Per avvio dall'ide
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        