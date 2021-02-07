# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:00:15 2021

@author: nicol
"""

import sys

import paths_info
from clustering import TRACK_AUDIO_COLUMNS, TRACK_META_NUMERICAL_COLUMNS, TRACK_META_TEXTUAL_COLUMNS

import pandas as pd

import pickle

def main(user, node_id):

    paths = paths_info.Path(user)
    
    paths.load_pack(pd.read_csv(paths.last_path))
            
    with open(paths.clusterer_dump, "rb") as file:
        clusterer = pickle.load(file)
        
    # ASSEGNAMENTI UTILI
    model = clusterer.model
    track = clusterer.dataset['track']
    data_track = track[TRACK_AUDIO_COLUMNS + TRACK_META_NUMERICAL_COLUMNS]   # separo le informazioni numeriche
    data_meta = track[TRACK_META_TEXTUAL_COLUMNS]  # separo le informazioni testuali
    data = [data_track, data_meta]
    
    current_node = get_node(model.root_, node_id)
    return_clusters(current_node, data, clusterer.audio_relevant_columns, paths, 'track')
     
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

        
def return_clusters(node, data, columns, paths, scope):
    # Cancello il precedente return
    paths.delete_saved_clusters(paths.track_clust)
    
    # Salvo i centroidi
    centroids_df = pd.DataFrame(data = node.centroids_, columns = columns)
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
                print("Errore salvando la parte track dei clusters")
        
        

if __name__=="__main__":
    # main(sys.argv[1], sys.argv[2])
    main('nic', "011")     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        