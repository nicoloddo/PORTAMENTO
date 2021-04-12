import os
import pandas as pd
import json
import glob

DATASET_README = "Qui dentro il dump è importante per il ricaricamento del dataset, mentre"

# DEFAULTS ***************************************************************************************************************************
DEFAULT_SETTINGS = {    # CI SI RIFERISCE AI PRESET ATTRAVERSO I LORO IDs.
        'axis'    : 'default',
        'dataset' : 'default',
        'weights' : 'default'
        }

DEFAULT_AUDIO_BLACKLIST = "loudness\nkey\nmode\ntime_signature\n"
DEFAULT_TEXTUAL_BLACKLIST = ""
DEFAULT_TRACK_BLACKLIST = DEFAULT_AUDIO_BLACKLIST + DEFAULT_TEXTUAL_BLACKLIST + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."
DEFAULT_SECTIONS_BLACKLIST = "" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."
DEFAULT_SEGMENTS_BLACKLIST = "loudness_end\n" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."

# DEFAULT TABLES
WEIGHTS1 = {
        # I WEIGHTS SONO IN JSON
        'weights' : """{
            "acousticness"        :0.7, 
            "danceability"        :0.7,
            "energy"              :1,
            "instrumentalness"    :0.50,
            "key"                 :0.35,
            "liveness"            :0.2,
            "loudness"            :1,
            "mode"                :1,
            "speechiness"         :1,
            "tempo"               :1,
            "time_signature"      :1,
            "valence"             :1}""",
        'name' : 'default',
        'description' : 'Optimal weights to obtain a classic genre-like clusterization.',
        'id' : 'default'
}
WEIGHTS2 = {
        # I WEIGHTS SONO IN JSON
        'weights' : """{
            "acousticness"        :0.7, 
            "danceability"        :0.7,
            "energy"              :0.6,
            "instrumentalness"    :0.50,
            "key"                 :0.35,
            "liveness"            :0.2,
            "loudness"            :1,
            "mode"                :1,
            "speechiness"         :1,
            "tempo"               :1,
            "time_signature"      :1,
            "valence"             :1}""",
        'name' : 'maybe_default',
        'description' : 'Optimal weights to obtain a classic genre-like clusterization.',
        'id' : 'good'
}
WEIGHTS3 = {
        # I WEIGHTS SONO IN JSON
        'weights' : """{
            "acousticness"        :1, 
            "danceability"        :1,
            "energy"              :1,
            "instrumentalness"    :1,
            "key"                 :1,
            "liveness"            :1,
            "loudness"            :1,
            "mode"                :1,
            "speechiness"         :1,
            "tempo"               :1,
            "time_signature"      :1,
            "valence"             :1}""",
        'name' : 'all ones',
        'description' : 'All the features considered equally.',
        'id' : 'all_1'
}
DEFAULT_WEIGHTS = pd.DataFrame()
DEFAULT_WEIGHTS = DEFAULT_WEIGHTS.append(WEIGHTS1, ignore_index=True)
DEFAULT_WEIGHTS = DEFAULT_WEIGHTS.append(WEIGHTS2, ignore_index=True)



DATASET1 = {
        'name' : 'default',
        'id'   : 'default'
        }
DEFAULT_DATASETS = pd.DataFrame()
DEFAULT_DATASETS = DEFAULT_DATASETS.append(DATASET1, ignore_index=True)


AXIS1 = {
        'axis1': 'valence',
        'axis2': 'energy',
        'axis3': 'tempo',
        'name' : 'default',
        'id'   : 'default'
        }
DEFAULT_AXIS = pd.DataFrame()
DEFAULT_AXIS = DEFAULT_AXIS.append(AXIS1, ignore_index=True)

#*************************************************************************************************************************************

# ESTENSIONI BASE
CONTROL_EXT = ".txt"
DATAFRAME_EXT = ".csv"
DUMP_EXT = ".sav"

class Path:
    
    songpack = []
    
    def __init__(self, user, root):    
        
        # COSTRUISCO IL PATH BASE
        self.root = root
        self.base = self.root + r'\users\nic'
        
        # COLLEGO IL PATH DEL LAST_PATH CHE SERVE ALL'INTERFACCIA
        self.last_path = os.path.join(self.root, r'last_path' + DATAFRAME_EXT)
        
        
        # COLLEGO I PATH DELLE CARTELLE DI BASE E LE CREO SE NON SON STATE CREATE.
        self.bundles_path = os.path.join(self.base, r'bundles')
        self.mkdir_if_not(self.bundles_path)
        self.datasets_path = os.path.join(self.base, r'datasets')
        self.mkdir_if_not(self.datasets_path)
        self.tables = os.path.join(self.base, r'tables')
        self.mkdir_if_not(self.tables)
        self.radars = os.path.join(self.base, r'radars')
        self.mkdir_if_not(self.radars)
        
        
        # COLLEGO I PATH DEI FILE DI DEFAULT
        self.oauth = os.path.join(self.base, r'oauth' + CONTROL_EXT)    # Costruisco il path del file dell'oauth token
        self.refresh_token = os.path.join(self.base, r'refresh_token' + CONTROL_EXT)    # Costruisco il path del file del refresh token         
            
        self.settings = os.path.join(self.base, r'settings' + CONTROL_EXT)
        self.weights_table = os.path.join(self.tables, r'weights_table' +  DATAFRAME_EXT)
        self.datasets_table = os.path.join(self.tables, r'datasets_table' +  DATAFRAME_EXT)
        self.axis_table = os.path.join(self.tables, r'axis_table' +  DATAFRAME_EXT)
        
        # CREO I FILE SE NON E' STATA AVVIATA L'INSTALLAZIONE
        # OAUTH
        self.txt_if_not(self.oauth, "")
        self.txt_if_not(self.refresh_token, "")
        
        # SETTINGS
        self.json_if_not(self.settings, DEFAULT_SETTINGS)
 
        # TABLES
        self.csv_if_not(self.weights_table, DEFAULT_WEIGHTS)
        self.csv_if_not(self.datasets_table, DEFAULT_DATASETS)
        self.csv_if_not(self.axis_table, DEFAULT_AXIS)
    #------------------------------------------------------------------------------------------------------------------------------
    def initialize_default_files(self):   # Attenzione: questa funzione sovrascrive, è da chiamare solo in caso di reinstallazione
        
        # OAUTH
        self.txt_install(self.oauth, "")
        self.txt_install(self.refresh_token, "")
        
        # SETTINGS
        self.json_install(self.settings, DEFAULT_SETTINGS)
            
        # TABLES
        self.csv_install(self.weights_table, DEFAULT_WEIGHTS)
        self.csv_install(self.datasets_table, DEFAULT_DATASETS)
        self.csv_install(self.axis_table, DEFAULT_AXIS)
    
    #******************************************************************************************************************************    
    def link_database(self, bundle_name):   
        # CREO L'ELENCO DI PATH DA CREARE PER OGNI PLAYLIST
        self.path_name = [                    
                        'sections',  #  - sezioni
                        'sections_confidences',  #  - sections_confidences
                        'segments',  #  - segmenti
                        'segments_confidences',  #  - segments_confidences
                        # 'segments_clust', #  - cluster segment
                        'n_songs']    #  - numero di canzoni  
        
        # CREO I PATH PER IL NUOVO DATABASE
        self.bundle = os.path.join(self.bundles_path, bundle_name)    # Il path dal quale l'user può comandare gli input del software (playlist packs e blacklists)
        self.mkdir_if_not(self.bundle)
            
        self.dataset = os.path.join(self.datasets_path, bundle_name)  # Il path del nuovo dataset
        self.mkdir_if_not(self.dataset)
            
        self.models = os.path.join(self.dataset, r'models')  # Il path dove salvo i modelli pickle dopo la clusterizzazione
        self.mkdir_if_not(self.models)
        
        
        # GLI UNICI FILE CHE CREO E INIZIALIZZO GIA' (E IL CUI PATH COMPRENDE L'ESTENSIONE) SON QUELLI CONTROLLABILI DALL'UTENTE NELLA CARTELLA BUNDLES
        self.initialize_default_dataset_files(bundle_name)        
        
        
        # CREO LA CARTELLA IN CUI RESTITUIRE I TRACK CLUSTERS DIVISI PER URI
        self.track_uri_clust = os.path.join(self.bundle, r'track_clust')
        if(not os.path.isdir(self.track_uri_clust)):
            os.mkdir(self.track_uri_clust)
        
        # CREO LA CARTELLA IN CUI RESTITUIRE I CLUSTERS DIVISI IN DATASETS
        self.track_final_clust = os.path.join(self.dataset, r'final_clust')
        if(not os.path.isdir(self.track_final_clust)):
            os.mkdir(self.track_final_clust)
            
        # CREO LA CARTELLA IN CUI RESTITUIRE I CLUSTERS DEL NODO DA VISUALIZZARE DIVISI IN DATASET
        self.track_clust = os.path.join(self.dataset, r'clust')
        if(not os.path.isdir(self.track_clust)):
            os.mkdir(self.track_clust)
            
        # FILE IN CUI SALVO I DUMP DEL MODELLO, DEL DATASET E DEL CLUSTERER
        self.model = os.path.join(self.models, r'model_') # Il nome del file andrà completato e aggiornato nel momento del salvataggio
        self.dataset_dump = os.path.join(self.dataset, r'dataset_dump' + DUMP_EXT)
        self.clusterer_dump = os.path.join(self.track_final_clust, r'clusterer_dump' + DUMP_EXT)
        
        # FILE IN CUI SALVO I CENTROIDI
        self.centroids = os.path.join(self.track_clust, r'centroids' + DATAFRAME_EXT)
        self.final_centroids = os.path.join(self.track_final_clust, r'final_centroids' + DATAFRAME_EXT)
    
    #------------------------------------------------------------------------
        # DA QUI CREO IL PATH PER I FILE IN CUI RESTITUIRE IL DATASET LEGGIBILE (COMPRESA LA FUNZIONE SEGUENTE CHE CHIAMO PROPRIO QUI SOTTO)
        self.track = os.path.join(self.bundle, r'track')
        self.track_confidences = os.path.join(self.bundle, r'track_confidences')
        self.albums = os.path.join(self.bundle, r'albums')
        self.artists = os.path.join(self.bundle, r'artists')
        self.n_playlists = os.path.join(self.bundle, r'n_playlists')
        
        
        # Costruisco i path di ogni playlist
        with open(self.playlistpack, "r") as playlist_pack:
            for playlist_num, playlist in enumerate(playlist_pack):
                self.build_playlistpath(playlist_num)

    
    def link_radar(self, radar_name):
        
        #CREO O COLLEGO IL FILE RADARPACK
        self.radarpack = os.path.join(self.radars, radar_name + CONTROL_EXT)    # Costruisco il path del file playlist_pack in cui bisogna inserire tutti i link alle playlist
        self.txt_if_not(self.radarpack, "")
        
        # CREO O COLLEGO LA CARTELLA DOVE RILASCIARE I DUMP
        self.radar_dumps = os.path.join(self.radars, r'radar_dumps')
        if(not os.path.isdir(self.radar_dumps)):
            os.mkdir(self.radar_dumps)
        
        # CREO O COLLEGO IL FILE DOVE SALVARE E CARICARE IL DUMP
        self.radar_dump = os.path.join(self.radar_dumps, radar_name + DUMP_EXT)
    
    #************************************************************************************************************************************
    def build_playlistpath(self, playlist_num):
          
        playlist_path = os.path.join(self.bundle, str(playlist_num))    # Il path di ogni playlist del bundle
        if(not os.path.isdir(playlist_path)):
                os.mkdir(playlist_path)

        # Creo le directory di ogni playlist
        self.songpack.append(  
                        {
                        
                        self.path_name[i] : os.path.join(playlist_path, self.path_name[i]) for i in range(len(self.path_name) -1)    # Costruisco i path base a parte che per quello del songpack
                    
                        }
                       )
        
        for key, path in self.songpack[-1].items():  # creo le cartelle dell'ultimo songpack creato
            self.mkdir_if_not(path)
        
        self.songpack[-1]['path'] = playlist_path
        self.songpack[-1]['n_songs'] = os.path.join(playlist_path, r'n_songs')     # Costruisco il path del songpack del file songpack (il -1 è per aggiungere al dizionario appena messo nella lista)
    
    def save_playlist_name(self, count_pl, name, link):
        self.txt_if_not(os.path.join(self.songpack[count_pl]['path'], name) + CONTROL_EXT, link)
        
    #************************************************************************************************************************************
    def changes_history_path(self):
        
        playlists_changes_history = os.path.join(self.bundle, r'playlists_changes_history')  # Il path del nuovo dataset
        self.mkdir_if_not(playlists_changes_history)
        return playlists_changes_history
    
    def save_history(self, data, to_what):
        path = os.path.join(self.changes_history_path(), to_what)
        count = 0
        while True:
            temp = path + str(count) + DATAFRAME_EXT
            if self.csv_if_not(temp, data) is True:
                break
            else:
                count = count + 1
                
    #************************************************************************************************************************************
    def mkdir_if_not(self, path):     # controlla se la cartella esiste, se non esiste la crea
        if(not os.path.isdir(path)):
            os.mkdir(path)
    
    def txt_install(self, path, default_data):
        crea = open(path, "w+")
        crea.write(default_data)
        crea.close()
    def txt_if_not(self, path, data):
        if(not os.path.isfile(path)):
            self.txt_install(path, data)
    
    def csv_install(self, path, default_data):  # default_data qui deve essere un dataframe!
        salva = open(path, "w+")
        export_csv = default_data.to_csv (path, index = None, header=True)    # Esporto il dataset
        if str(export_csv) != 'None':
            print("Errore salvando una table di default. Path: " + path)
        salva.close()
    def csv_if_not(self, path, data):   
        if(not os.path.isfile(path)):
            self.csv_install(path, data)
            return True
        else:
            return False
    
    
    def json_install(self, path, default_data):
        with open(path, 'w+') as salva:
            json.dump(DEFAULT_SETTINGS, salva, sort_keys=True, indent=4)
    def json_if_not(self, path, default_data):
        if(not os.path.isfile(path)):
            self.json_install(path, default_data)
    
    #*************************************************************************************************************************************        
    def initialize_default_dataset_files(self, bundle_name):
        
        #CREO IL FILE PLAYLISTPACK
        self.playlistpack = os.path.join(self.bundle, bundle_name + CONTROL_EXT)    # Costruisco il path del file playlist_pack in cui bisogna inserire tutti i link alle playlist
        self.txt_if_not(self.playlistpack, "")
           
        # PATHS BLACKLISTS
        self.track_blacklist = os.path.join(self.bundle, r'track_blacklist' + CONTROL_EXT) # Costruisco il path del FILE TRACK BLACKLIST
        self.txt_if_not(self.track_blacklist, DEFAULT_TRACK_BLACKLIST)

        self.sections_blacklist = os.path.join(self.bundle, r'sections_blacklist' + CONTROL_EXT) # Costruisco il path FILE SECTIONS BLACKLIST
        self.txt_if_not(self.sections_blacklist, DEFAULT_SECTIONS_BLACKLIST)

        self.segments_blacklist = os.path.join(self.bundle, r'segments_blacklist' + CONTROL_EXT) # Costruisco il path del FILE SEGMENTS BLACKLIST 
        self.txt_if_not(self.segments_blacklist, DEFAULT_SEGMENTS_BLACKLIST)
        
        
    #*************************************************************************************************************************************
    def delete_saved_clusters(self, cluster_path):
        
        files = glob.glob(cluster_path + '\*')
        for f in files:
            os.remove(f)
    
    #*************************************************************************************************************************************
    def pack_paths(self):
        pack = pd.DataFrame(self.__dict__)
        pack = pack[:1]
        
        with open(self.last_path, "w+"):
            export_csv = pack.to_csv (self.last_path, index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando il last_paths.")
    
    #*************************************************************************************************************************************    
    def load_pack(self, last_paths):
        # CARICA UN PACK_PATH SALVATO
        for key in last_paths:
            self.__dict__[key] = last_paths[key][0]
        
        
        