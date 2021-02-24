# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:19:13 2020

@author: nicol
"""

# PER GESTIRE I DATASET
import pandas as pd
import numpy as np

# PER LA CLUSTERIZZAZIONE
from sklearn.cluster import AgglomerativeClustering
from birch_mod import Birch

# PER IL SALVATAGGIO DEL MODELLO
import pickle

# PER LA VISUALIZZAZIONE
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

TRACK_AUDIO_COLUMNS = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'] # AUDIO FEATURES
TRACK_META_TEXTUAL_COLUMNS = ['album', 'album_id', 'artist', 'artists_id', 'disc_number', 'id', 'name', 'playlist', 'preview_url', 'track_number', 'uri']  # QUESTE SONO LE TEXTUAL FEATURES, DA SEPARARE DA QUELLE AUDIO
TRACK_META_NUMERICAL_COLUMNS = ['duration_ms', 'popularity']
TRACK_TEXTUAL_COLUMNS = TRACK_META_TEXTUAL_COLUMNS + TRACK_META_NUMERICAL_COLUMNS
# ATTENZONE !! SE UNA FEATURE NON COMPARE TRA QUELLE SOPRA, NON SARA' MAI CONSIDERATA!!!

TRACK_DEFAULT_BLACKLIST = []
TRACK_DEFAULT_WHITELIST = ['danceability', 'tempo', 'energy']

# MODALITA' DI ESTRAPOLAZIONE DELLE COLONNE RILEVANTI
DEFAULT_AUDIO_COLUMNS_MODE = 'black'

# RANGE DI NORMALIZZAZIONI
tempo_range = {'min' : 0, 'max' : 250}

# SCALA DEI WEIGHT
WEIGHT_MAX = 10
        
class Clusterer:
    
    #*********************** INIT
    def __init__(self, data_in = None, weights_preset = 'default', save_final_clusters = False, return_clusters = True):
        
        self.return_clusters = return_clusters
        self.save_final_clusters = save_final_clusters
        
        # SPACCHETTO IL DATASET DALL'OGGETTO DATA IN ENTRATA
        if type(data_in) is dict:
            self.dataset = data_in    # dataset originale passato per referenza
        else:
            self.dataset = {'track':data_in, 'artists':{}, 'albums':{}}     # Se il dataset in entrata è solo il dataframe delle features
        # RICORDA DI STAR ATTENTO A EFFETTUARE OPERAZIONI DIRETTAMENTE SUL DATASET IN QUANTO MI TOCCHEREBBE RICARICARLO SE POI MI SERVE QUEL CHE HO CANCELLATO
        
        self.audio_relevant_columns = []   # colonne non filtrate dalla blacklist o whitelist, ossia le colonne audio che consideriamo rilevanti
        self.weights = weights_preset    # salvo nel clusterer le impostazioni di weighting
        
        
    def cluster_new_dataset(self, paths, birch_threshold = 0.2, branch_factor = 5, n_clusters_birch = None, algorithm = 'birch'):
        
        #************************************************** CLUSTERING DI 'TRACK'
        track = self.dataset['track']
        print(track.shape)
        
        audio = track[TRACK_AUDIO_COLUMNS]
        self.audio_relevant_columns = self.get_relevant_columns(paths, 'audio')
        
        # PREPROCESSING
        audio = audio[self.audio_relevant_columns]  # filtro le colonne
        self.filter_weights()   # filtro le stesse colonne dai weights
        audio = self.format_dataset(audio)    # formatto (per ora normalizzazione dei bpm e applicazione weights)
        self.dataset['track'].update(audio)  # aggiorno il dataset dopo i pesi e le normalizzazioni
        data_array = audio.to_numpy()    # linearizzo perchè serve alla funzione di clusterizzazione
        
        # CLUSTERIZZAZIONE
        if algorithm == 'birch':
            model = Birch(threshold = birch_threshold, branching_factor = branch_factor, n_clusters = n_clusters_birch)
            model.fit(data_array)  # Clusterizzo
            centroids = model.subcluster_centers_    # Estraggo i centroidi
            n_clusters = centroids.shape[0]
        

        labels = model.labels_   # Estraggo il vettore che indica in quale cluster è finita ogni canzone.
        
        
        # ************************SALVATAGGIO
        
        # Salvo il modello
        with open(paths.model + self.weights['id'] + ".sav", "wb+") as salva:
            pickle.dump(model, salva) 
        paths.model = paths.model + self.weights['id'] + ".sav"    # Aggiorno il percorso in cui si trova il dump
        
        # Salvo il Clusterer
        self.model = model    # Aggiungo il modello al clusterer prima di fare il dump
        with open(paths.clusterer_dump, "wb+") as salva:
            pickle.dump(self, salva)
        
        # Salvo i clusters
        if self.return_clusters == True:
            self.save_centroids(paths, centroids, audio)
            clusters = self.save_clusters(paths, n_clusters, labels, 'track')  # salvo i risultati del clustering track
        else:
            clusters = []
        
        
        # PLOTTING
        plotting = False
        if plotting == True:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(track[self.audio_relevant_columns[0]], track[self.audio_relevant_columns[1]], track[self.audio_relevant_columns[2]], c= model.labels_.astype(float), s=50)
            ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], c='red', marker = 'X', s=50)
            plt.show()
        
        return clusters
    
    #**************************************************        
    def get_relevant_columns(self, paths, scope, mode = DEFAULT_AUDIO_COLUMNS_MODE):    # restituisce le colonne rilevanti tra quelle testuali o audio.
        
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
        salva_track = []    # lista in cui salvo i riferimenti ai file csv track di ogni cluster, ossia con le informazioni audio
        salva_meta = []    # lista in cui salvo i riferimenti ai file csv meta di ogni cluster, ossia le informazioni testuali
        
        rows = [] # matrice in cui divido le canzoni tra ogni cluster per indice (per ora è solo una lista ma creo una matrice nel prossimo for)
        clusters = []   # lista di dataframe con ogni cluster separato
        
        clusterized_df = self.dataset[scope]
        
        for i in range(n_clusters): # Inizializzazione dei vettori
            if(self.save_final_clusters):
                salva.append(open(paths.__dict__[scope + '_uri_clust'] + r'\cluster' + str(i) + ".txt", "w+"))
                salva_track.append(open(paths.__dict__[scope + '_final_clust'] + r'\track' + str(i) + ".csv", "w+"))
                salva_meta.append(open(paths.__dict__[scope + '_final_clust'] + r'\meta' + str(i) + ".csv", "w+"))
            rows.append([])
        
        for song_index, label in enumerate(labels):
            if(self.save_final_clusters):
                song_id = clusterized_df.at[song_index, 'id']
                uri = "spotify:track:" + song_id
                salva[label].write(uri + '\n')
            rows[label].append(song_index)    # mi segno la canzone nella riga giusta
            
        for i in range(n_clusters): # Chiudo i files             
             clusters.append(clusterized_df.iloc[rows[i], :])  # seleziono le canzoni del dataframe seguendo lo smistamento di rows: avrò ora un dataframe per ogni cluster
             cluster_track = clusters[i][TRACK_AUDIO_COLUMNS + TRACK_META_NUMERICAL_COLUMNS]   # separo le informazioni numeriche
             cluster_meta = clusters[i][TRACK_META_TEXTUAL_COLUMNS]  # separo le informazioni testuali
             
             if(self.save_final_clusters):
                 # salvo il dataset delle informazioni audio
                 export_csv = cluster_track.to_csv (paths.__dict__[scope + '_final_clust'] + r'\track' + str(i) + ".csv", index = None, header=True)    # Esporto il dataset
                 if str(export_csv) != 'None':
                     print("Errore salvando la parte track dei clusters")
                 
                 # salvo il dataset delle informazioni testuali
                 export_csv = cluster_meta.to_csv (paths.__dict__[scope + '_final_clust'] + r'\meta' + str(i) + ".csv", index = None, header=True)    # Esporto il dataset
                 if str(export_csv) != 'None':
                     print("Errore salvando la parte meta dei clusters") 
                
                 salva_track[i].close()
                 salva_meta[i].close()
                 salva[i].close()
        if(self.save_final_clusters):
            print("\n**I clusters son stati salvati nella cartella!**  PATH: " + paths.__dict__[scope + '_uri_clust'])
            print("\nUSA QUESTO STRUMENTO PER VEDERE LE CANZONI IN UN CLUSTER:")
            print("https://www.spotlistr.com/search/textbox") 
        
        return clusters
    
    def save_centroids(self, paths, centroids, audio):
        # Salvo i centroidi
        centroids_df = pd.DataFrame(data = centroids, columns = audio.columns)/WEIGHT_MAX
        
        with open(paths.final_centroids, "w+"):
            export_csv = centroids_df.to_csv (paths.final_centroids, index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando i centroidi.")
    
    #******************************************************
    def format_dataset(self, dataset):   # Funzione statica in cui decido cosa normalizzare
        
        if 'tempo' in self.audio_relevant_columns:
            self.normalize_column(dataset, tempo_range['min'], tempo_range['max'], 'tempo')
        
        dataset = self.weight_features(dataset)
        
        return dataset
        
    #-------------------------------
    def normalize_column(self, dataframe, min_value, max_value, column):  # porto tutti gli elementi della colonna a variare tra [0, 1]
        
        for row in range(len(dataframe.index)):  #len con quell'argomento restituisce il numero di righe
            trasla = dataframe.at[row, column] - min_value    # porto la scala ad avere 0 come minimo
            normalized = trasla / (max_value - min_value)
            dataframe.at[row, column] = normalized
    
    #-------------------------------        
    def weight_features(self, dataset):
        
        weighted = dataset.apply(self.__weight__, axis=1) # axis = 1 serve a farlo sulle righe anzichè sulle colonne
        return weighted
    
    def __weight__(self, x):    
        # La funzione che pesa i parametri è una semplice moltiplicazione. Si basa sul fatto che se io moltiplico per un numero basso una delle coordinate,
        # i punti saranno più vicini rispetto a quella coordinata e dunque verrà considerata meno influente rispetto alla suddivisione.
        weights_ = list(self.weights['weights'].values())
        return x * weights_
    
    def filter_weights(self):   # toglie i weight delle colonne che non consideravamo rilevanti
        for key in list(self.weights['weights'].keys()):    # è scritto così perchè non posso iterare su un dizionario mentre gli cambio la dimensione
            if key not in self.audio_relevant_columns:
                del self.weights['weights'][key]
                
    #****************************************************************************************************************************************************** # TODO: CONTROLLA BENE MA MISSA' CHE QUESTA NON LA STO USANDO QUI MA IN clusters_dataset.py
    def predict(self, paths, model, algorithm = 'birch'):
        
        track = self.dataset['track']
        
        audio = track[TRACK_AUDIO_COLUMNS]
        self.audio_relevant_columns = self.get_relevant_columns(paths,'audio')
        
        # PREPROCESSING
        audio = audio[self.audio_relevant_columns]  # filtro le colonne
        self.filter_weights()   # filtro le stesse colonne dai weights
        audio = self.format_dataset(audio)    # formatto (per ora normalizzazione dei bpm e applicazione weights)
        
        labels = model.predict(audio)
        
        return labels
    
    
    
    