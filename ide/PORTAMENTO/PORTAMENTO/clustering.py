# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:19:13 2020

@author: nicol
"""

# PER GESTIRE I DATASET
import pandas as pd
import numpy as np

# PER LA CLUSTERIZZAZIONE
from sklearn.cluster import KMeans

# PER IL SALVATAGGIO DEL MODELLO
import pickle

# PER LA VISUALIZZAZIONE
import matplotlib.pyplot as plt

TRACK_AUDIO_COLUMNS = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'] # AUDIO FEATURES
TRACK_TEXTUAL_COLUMNS = ['album_id', 'artists_id', 'disc_number', 'duration_ms', 'id', 'name', 'playlist', 'popularity', 'track_number']  # QUESTE SONO LE TEXTUAL FEATURES, DA SEPARARE DA QUELLE AUDIO
# ATTENZONE !! SE UNA FEATURE NON COMPARE TRA QUELLE SOPRA, NON SARA' MAI CONSIDERATA!!!

TRACK_DEFAULT_BLACKLIST = []
TRACK_DEFAULT_WHITELIST = ['danceability', 'tempo', 'energy']

class Clusterer:
    
    #*********************** INIT
    def __init__(self, data_in, weights_preset):
        
        # SPACCHETTO IL DATASET DALL'OGGETTO DATA IN ENTRATA
        self.dataset = data_in    # dataset originale passato per referenza
        # RICORDA DI STAR ATTENTO A EFFETTUARE OPERAZIONI DIRETTAMENTE SUL DATASET IN QUANTO MI TOCCHEREBBE RICARICARLO SE POI MI SERVE QUEL CHE HO CANCELLATO
        
        self.audio_relevant_columns = []   # colonne non filtrate dalla blacklist o whitelist, ossia le colonne audio che consideriamo rilevanti
        self.weights = weights_preset    # salvo nel clusterer le impostazioni di weighting
        
    def cluster_new_dataset(self, paths, n_clusters = 8):
        
        # SCELGO MODALITA' DI ESTRAPOLAZIONE DELLE COLONNE RILEVANTI
        AUDIO_COLUMNS_MODE = 'white'
        
        #************************************************** CLUSTERING DI 'TRACK'
        track = self.dataset['track']
        print(track.shape)
        
        audio = track[TRACK_AUDIO_COLUMNS]
        self.audio_relevant_columns = self.get_relevant_columns(paths, AUDIO_COLUMNS_MODE, 'audio')
        
        # PREPROCESSING
        audio = track[self.audio_relevant_columns]  # filtro le colonne
        self.filter_weights()   # filtro le stesse colonne dai weights
        audio = self.format_dataset(audio)    # formatto (per ora normalizzazione dei bpm e applicazione weights)
        self.dataset['track'].update(audio)  # aggiorno il dataset con i pesi e le normalizzazioni
        data_array = audio.to_numpy()    # linearizzo perchè serve alla funzione kmeans
        
        # CLUSTERIZZAZIONE
        model = KMeans(n_clusters=n_clusters).fit(data_array)  # Clusterizzo
        centroids = model.cluster_centers_    # Estraggo cluster_centers dalla clusterizzazione
        labels = model.labels_   # Estraggo il vettore che indica in quale cluster è finita ogni canzone.
        
        # SALVATAGGIO
        with open(paths.model + self.weights['id'] + ".sav", "wb+") as salva:
            pickle.dump(model, salva)
        clusters = self.save_clusters(paths, n_clusters, labels, 'track')  # salvo i risultati del clustering track
        
        
        # PLOTTING
        plotting = True
        if plotting == True:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(track[self.audio_relevant_columns[0]], track[self.audio_relevant_columns[1]], track[self.audio_relevant_columns[2]], c= model.labels_.astype(float), s=50)
            ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', marker = 'X', s=50)
            plt.show()
        
        return clusters
    
    #**************************************************        
    def get_relevant_columns(self, paths, mode, scope):    # restituisce le colonne rilevanti tra quelle testuali o audio.
        
        track_blacklist = self.get_blacklist(paths, 'track', mode)
        track_whitelist = []
        
        track_blacklist.extend(TRACK_DEFAULT_BLACKLIST)
        track_whitelist.extend(TRACK_DEFAULT_WHITELIST)
        
        relevant_columns = []
        
        try:
            if scope == 'audio':
                COLUMNS = TRACK_AUDIO_COLUMNS
            elif scope == 'textual':
                COLUMNS = TRACK_TEXTUAL_COLUMNS
            else:
                raise ValueError
        except ValueError:
            assert False, "Scope colonne rilevanti definita erroneamente"
            
        try:
            if mode == 'white':
                relevant_columns = track_whitelist
            elif mode == 'black':
                # OTTENGO LE RILEVANTI DALL'INSIEME DELLE COLONNE
                for column in COLUMNS:
                    if column not in track_blacklist:
                        relevant_columns.append(column)
            else:
                raise ValueError
        except ValueError:
            assert False, "Modalità di estrapolazione colonne rilevanti definita erroneamente"
       
        return relevant_columns
            
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
    def format_dataset(self, dataset):   # Funzione statica in cui decido cosa normalizzare
        
        tempo_range = {'min' : 0, 'max' : 250}
        
        if 'tempo' in self.audio_relevant_columns:
            self.normalize_column(dataset, tempo_range['min'], tempo_range['max'], 'tempo')
        
        dataset = self.weight_features(dataset)
        
        return dataset
        
    #-------------------------------
    def normalize_column(self, dataframe, min_value, max_value, column):  # porto tutti gli elementi della colonna a variare tra [0, 1]
        
        for row in range(len(dataframe.index)):  #len con quell'argomento restituisce il numero di righe
            trasla = dataframe.get_value(row, column) - min_value    # porto la scala ad avere 0 come minimo
            normalized = trasla / (max_value - min_value)
            dataframe.at[row, column] = normalized
    
    #-------------------------------        
    def weight_features(self, dataset):
        
        weighted = dataset.apply(self.__weight__, axis=1) # axis = 1 serve a farlo sulle righe anzichè sulle colonne
        return weighted
    
    def __weight__(self, x):
        weights_ = list(self.weights['weights'].values())
        return x * weights_
    
    def filter_weights(self):   # toglie i weight delle colonne che non consideravamo rilevanti
        for key in list(self.weights['weights'].keys()):    # è scritto così perchè non posso iterare su un dizionario mentre gli cambio la dimensione
            if key not in self.audio_relevant_columns:
                del self.weights['weights'][key]