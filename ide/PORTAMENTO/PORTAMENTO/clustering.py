# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:19:13 2020

@author: nicol
"""

# import copy
import os

# PER GESTIRE I DATASET
import pandas as pd
import numpy as np

# PER LA CLUSTERIZZAZIONE
from sklearn.cluster import KMeans

# PER LA VISUALIZZAZIONE
import matplotlib.pyplot as plt


TRACK_DEFAULT_BLACKLIST = ['album_id', 'artists_id', 'disc_number', 'id', 'name', 'playlist', 'track_number']
TRACK_DEFAULT_WHITELIST = ['danceability', 'tempo', 'valence', 'energy', 'instrumentalness']

class Clusterer:
    
    dataset = {}
    
    
    #*********************** INIT
    def __init__(self, data_in):
        
        # SPACCHETTO IL DATASET DALL'OGGETTO DATA IN ENTRATA
        self.dataset = data_in.dataset    # dataset originale passato per referenza
        # RICORDA DI NON EFFETTUARE OPERAZIONI DIRETTAMENTE SUL DATASET IN QUANTO MI TOCCHEREBBE RICARICARLO SE POI MI SERVE QUEL CHE HO CANCELLATO
        
        self.relevant_columns = []   # colonne non filtrate dalla blacklist o whitelist
        
    def start(self, paths, n_clusters = 8):
        
        # SCELGO MODALITA' DI ESTRAPOLAZIONE DELLE COLONNE RILEVANTI
        RELEVANT_COLUMNS_MODE = 'white'
        
        #************************************************** CLUSTERING DI 'TRACK'
        track = self.dataset['track']
        print(track.shape)
        
        self.build_relevant_columns(paths, RELEVANT_COLUMNS_MODE)
        
        # PREPROCESSING
        self.format_dataset()    # formatto (per ora normalizzazione)
        filtered = track[self.relevant_columns]  # filtro le colonne
        data_array = filtered.to_numpy()    # linearizzo perchè serve alla funzione kmeans
        
        
        # CLUSTERIZZAZIONE
        kmeans = KMeans(n_clusters=n_clusters).fit(data_array)  # Clusterizzo
        centroids = kmeans.cluster_centers_    # Estraggo cluster_centers dalla clusterizzazione
        labels = kmeans.labels_   # Estraggo il vettore che indica in quale cluster è finita ogni canzone.
        
        # SALVATAGGIO
        clusters = self.save_clusters(paths, n_clusters, labels, 'track')  # salvo i risultati del clustering track
        
        
        # PLOTTING
        plt.scatter(track[self.relevant_columns[0]], track[self.relevant_columns[1]], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
        plt.show()
        
        return clusters
    
    #**************************************************
    def build_relevant_columns(self, paths, mode):    # restituisce le colonne rilevanti a partire da una blacklist di colonne
        
        track_blacklist = self.get_blacklist(paths, 'track', mode)
        track_whitelist = []
        
        track_blacklist.extend(TRACK_DEFAULT_BLACKLIST)
        track_whitelist.extend(TRACK_DEFAULT_WHITELIST)
        
        try:
            if mode == 'white':
                self.relevant_columns = track_whitelist
            elif mode == 'black':
                # OTTENGO LE RILEVANTI DALL'INSIEME DELLE COLONNE
                for column in self.dataset['track']:
                    if column not in track_blacklist:
                        self.relevant_columns.append(column)
            else:
                raise ValueError
        except ValueError:
            assert False, "Modalità di estrapolazione colonne rilevanti definita erroneamente"
        
            
    #**************************************************    
    def get_blacklist(self, paths, scope, mode):  # Estrae i parametri da filtrare dal file di blacklist o whitelist
        # LO SCOPE PUO' ESSERE 'track', 'sections', 'segments' ECC 
        
        filterlist = []     # lista con ulteriori parametri da filtrare oltre a quelli di default
        
        print("\nSto filtrando questi parametri da " + scope + ": ")
        
        with open(paths.__dict__[scope + "_blacklist"], "r") as to_filter:   #Filtro i parametri della clusterizzazione di track.
            for thing in to_filter:
                if 'FINE' in thing:
                    break
                
                thing = thing[:-1]  # Tolgo l'ultimo carattere che sarà o un \n o un carattere EOF perchè creerebbe problemi
                
                # STAMPO COSA STO FILTRANDO
                print(thing)
                
                try:
                # CONTROLLO
                    if thing not in self.dataset[scope]:
                        raise ValueError
                        # AGGIUNGO ALLA LISTA DI FILTRAGGIO
                    else:
                        filterlist.append(thing)
                except ValueError:
                    assert False, "ERRORE!!! - La blacklist contenuta nella cartella della playlist non è valida! Ricorda che i parametri vanno uno per riga"
        
        return filterlist
    
    #****************************************************
    def save_clusters(self, paths, n_clusters, labels, scope):  # Funzione che smista le canzoni e le salva in files: un file per cluster.
        
        salva = []      # lista in cui salvo tutti i riferimenti ai file di ogni cluster: salverò infatti gli uri di ogni cluster in un separato file
        
        rows = [] # matrice in cui divido le canzoni tra ogni cluster per indice (per ora è solo una lista ma creo una matrice nel prossimo for)
        clusters = []   # lista di dataframe con ogni cluster separato
        
        clusterized_df = self.dataset[scope]
        
        for i in range(n_clusters): # Inizializzazione dei vettori
             salva.append(open(paths.__dict__[scope + '_clust'] + r'\cluster' + str(i) + ".txt", "w+"))
             rows.append([])
        
        for song_index, label in enumerate(labels):
            song_id = clusterized_df.at[song_index, 'id']
            uri = "spotify:track:" + song_id
            salva[label].write(uri + '\n')
            
            rows[label].append(song_index)    # mi segno la canzone nella riga giusta
            
        for i in range(n_clusters): # Chiudo i files
             salva[i].close()
             clusters.append(clusterized_df.iloc[rows[i], :])  # seleziono le canzoni del dataframe seguendo lo smistamento di rows: avrò ora un dataframe per ogni cluster
        
        print("\n**I clusters son stati salvati nella cartella!**  PATH: " + paths.__dict__[scope + '_clust'])
        print("\nUSA QUESTO STRUMENTO PER VEDERE LE CANZONI IN UN CLUSTER:")
        print("https://www.spotlistr.com/search/textbox") 
        print("\nI risultati scarsi possono essere dovuti, oltre al numero basso di parametri utilizzati, al fatto che non sto ancora considerando l'accuracy dei parametri  le canzoni.")
        
        return clusters
    
    #******************************************************
    def format_dataset(self):
        
        tempo_range = {'min' : 0, 'max' : 250}
        
        if 'tempo' in self.relevant_columns:
            self.normalize_column(self.dataset['track'], tempo_range['min'], tempo_range['max'], 'tempo')
        
    #-------------------------------
    def normalize_column(self, dataframe, min_value, max_value, column):  # porto tutti gli elementi della colonna a variare tra [0, 1]
        
        for row in range(len(dataframe.index)):  #len con quell'argomento restituisce il numero di righe
            trasla = dataframe.get_value(row, column) - min_value    # porto la scala ad avere 0 come minimo
            normalized = trasla / (max_value - min_value)
            dataframe.at[row, column] = normalized
            