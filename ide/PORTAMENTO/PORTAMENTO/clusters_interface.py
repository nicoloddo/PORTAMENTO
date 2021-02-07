# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:00:15 2021

@author: nicol
"""

import sys

import paths_info
from clustering import TRACK_AUDIO_COLUMNS, TRACK_META_NUMERICAL_COLUMNS, TRACK_META_TEXTUAL_COLUMNS

import pandas as pd
import numpy as np

import pickle

# IMPORT PER IL PREDICT
from sklearn.utils import check_array
from sklearn.utils.extmath import safe_sparse_dot, row_norms

def main(user, node_id):

    last_path = paths_info.Path(user).last_path
    
    paths = pd.read_csv(last_path)
            
    with open(paths.clusterer_dump[0], "rb") as file:
        clusterer = pickle.load(file)
        cluster_in_inspector = [clusterer]  # TODO: da cancellare quando hai finito di fare debugging dello script
        
    # ASSEGNAMENTI UTILI
    model = clusterer.model
    track = clusterer.dataset['track']
    data_track = track[TRACK_AUDIO_COLUMNS + TRACK_META_NUMERICAL_COLUMNS]   # separo le informazioni numeriche
    data_meta = track[TRACK_META_TEXTUAL_COLUMNS]  # separo le informazioni testuali
    data = [data_track, data_meta]
    
    current_node = get_node(model.root_)
    return_clusters(current_node, data)
     
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

        
def return_clusters(node, data):
    
    
    
    pass
        
        

if __name__=="__main__":
    # main(sys.argv[1], sys.argv[2])
    main('nic', "0012")     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        