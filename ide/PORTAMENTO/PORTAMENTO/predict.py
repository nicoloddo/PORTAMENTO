# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 18:10:08 2021

@author: nicol
"""
# IMPORTO I PATHS
import paths_info

# IMPORTO I TABLES
import tables as tb

import pickle

import playlist_compass as comp

# IMPORTO LE UTILITIES DI CLUSTERING
import clustering as cl



def main():
    
    playlist_uri = "spotify:playlist:7fVARlHGTrSvkaNXhjSVxC"
    
    
    trip = {'weights': 'default', 'dataset': 'sounds_of_everything'}
    
    base_path = r'D:\PROJECTS\PORTAMENTO\users\nic'
    
    paths = paths_info.Path(base_path)    # COLLEGO I PATH ALLE MIE STRUTTURE
    paths.link_database(trip['dataset'])
    
    # IMPORTO I TABLES
    tables = tb.Tables(paths)
    # OTTENGO I WEIGHTS PER LA CLUSTERIZZAZIONE
    weights = tables.weights.get(trip['weights'])
    
    with open(paths.model + trip['weights'] + ".sav", "rb") as input_file:
        model = pickle.load(input_file)
    
    
    compass = comp.Playlist_compass(paths, playlist_uri).features
    
    # Creo il clusterer       
    clust = cl.Clusterer(compass, weights)
    labels = clust.predict(paths, model, 'birch')
    
    return 0
    
if __name__=="__main__":
    main()