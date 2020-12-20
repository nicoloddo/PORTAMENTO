import os
import pandas as pd

# DEFAULTS
DEFAULT_TRACK_BLACKLIST = "duration_ms\nloudness\nkey\nmode\npopularity\ntime_signature\n" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."
DEFAULT_TEXTUAL_BLACKLIST = "" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."
DEFAULT_SECTIONS_BLACKLIST = "" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."
DEFAULT_SEGMENTS_BLACKLIST = "loudness_end\n" + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST."

WEIGHTS = {
        "weights" : {
                "acousticness"        :1,
                "danceability"        :1,
                "energy"              :1,
                "instrumentalness"    :1,
                "key"                 :1,
                "liveness"            :1,
                "loudness"            :1,
                "mode"                :1,
                "popularity"          :1,
                "speechiness"         :1,
                "tempo"               :1,
                "time_signature"      :1,
                "valence"             :1,
                    },
        "name" : "default",
        "description" : "default",
}

DEFAULT_WEIGHTS = pd.DataFrame()
DEFAULT_WEIGHTS = DEFAULT_WEIGHTS.append(WEIGHTS, ignore_index=True)



# ESTENSIONI BASE
CONTROL_EXT = ".txt"
DATAFRAME_EXT = ".csv"

class Path:
    
    songpack = []
    
    def __init__(self, base):    
        self.path_name = [                    
                        'sections',  #  - sezioni
                        'sections_confidences',  #  - sections_confidences
                        'segments',  #  - segmenti
                        'segments_confidences',  #  - segments_confidences
                        # 'segments_clust', #  - cluster segment
                        'n_songs']    #  - numero di canzoni  
        
        # CREO I PATH DI BASE  SE NON SON STATI CREATI
        self.bundles_path = os.path.join(base, r'bundles')
        self.mkdir_if_not(self.bundles_path)
        self.datasets_path = os.path.join(base, r'datasets')
        self.mkdir_if_not(self.datasets_path)
        self.presets = os.path.join(base, r'presets')
        self.mkdir_if_not(self.presets)
        
        self.oauth = os.path.join(base, r'oauth' + CONTROL_EXT)    # Costruisco il path del file dell'oauth token            
        #CREO IL FILE DELL'OAUTH
        if(not os.path.isfile(self.oauth)):
            crea = open(self.oauth, "w+")
            crea.close()
        #------------------------------------------------------------------------------------------------------------------------------
    
    def new_database(self, bundle_name):    
        # CREO I PATH PER IL NUOVO DATABASE
        self.bundle = os.path.join(self.bundles_path, bundle_name)    # Il path dal quale l'user può comandare gli input del software (playlist packs e blacklists)
        self.mkdir_if_not(self.bundle)
            
        self.dataset = os.path.join(self.datasets_path, bundle_name)  # Il path del nuovo dataset
        self.mkdir_if_not(self.dataset)
            
        self.models = os.path.join(self.dataset, r'models')  # Il path dove salvo i modelli pickle dopo la clusterizzazione
        self.mkdir_if_not(self.models)
        
        
        # GLI UNICI FILE CHE CREO GIA' (E IL CUI PATH COMPRENDE L'ESTENSIONE) SON QUELLI CONTROLLABILI DALL'UTENTE NELLA CARTELLA BUNDLES
        #------------------------------------------------------------------------------------------------------------------------------
        self.playlistpack = os.path.join(self.bundle, bundle_name + CONTROL_EXT)    # Costruisco il path del file playlist_pack in cui bisogna inserire tutti i link alle playlist
        #CREO IL FILE PLAYLISTPACK
        if(not os.path.isfile(self.playlistpack)):
           crea = open(self.playlistpack, "w+")
           crea.close()
        
        # INIZIALIZZO BLACKLISTS E I PRESETS
        self.initialize_default_files()
        
        
        # CREO LA CARTELLA IN CUI RESTITUIRE I TRACK CLUSTERS
        self.track_clust = os.path.join(self.bundle, r'track_clust')
        if(not os.path.isdir(self.track_clust)):
            os.mkdir(self.track_clust)
    
    #------------------------------------------------------------------------------------------------------------------------------------
    # DA QUI CREO IL PATH PER I FILE IN CUI SALVARE IL DATASET (COMPRESA LA FUNZIONE SEGUENTE CHE CHIAMO PROPRIO QUI SOTTO)
        self.track = os.path.join(self.dataset, r'track')
        self.track_confidences = os.path.join(self.dataset, r'track_confidences')
        self.albums = os.path.join(self.dataset, r'albums')
        self.artists = os.path.join(self.dataset, r'artists')
        self.n_playlists = os.path.join(self.dataset, r'n_playlists')
        self.model = os.path.join(self.dataset, r'model')
        
        # Costruisco i path di ogni playlist
        with open(self.playlistpack, "r") as playlist_pack:
            for playlist_num, playlist in enumerate(playlist_pack):
                self.build_playlistpath(playlist_num)


    #************************************************************************************************************************************
    def build_playlistpath(self, playlist_num):
          
        playlist_path = os.path.join(self.dataset, str(playlist_num))    # Il path di ogni playlist del bundle
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
        
        self.songpack[-1]['n_songs'] = os.path.join(playlist_path, r'n_songs')     # Costruisco il path del songpack del file songpack (il -1 è per aggiungere al dizionario appena messo nella lista)
        
    
    #*************************************************************************************************************************************    
    def mkdir_if_not(self, path):     # controlla se la cartella esiste, se non esiste la crea
        if(not os.path.isdir(path)):
            os.mkdir(path)
    
    def txt_if_not(self, path, default_data):
        if(not os.path.isfile(path)):
            crea = open(path, "w+")
            crea.write(default_data)
            crea.close()
    
    def csv_if_not(self, path, default_data):   # default_data qui deve essere un dataframe!
        if(not os.path.isfile(path)):
            salva = open(path, "w+")
            export_csv = default_data.to_csv (path, index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando un preset di default. Path: " + path)
            salva.close()
    
    #*************************************************************************************************************************************        
    def initialize_default_files(self):
        
        # PATHS BLACKLISTS
        self.track_blacklist = os.path.join(self.bundle, r'track_blacklist' + CONTROL_EXT) # Costruisco il path del FILE TRACK BLACKLIST
        self.file_if_not(self.track_blacklist, DEFAULT_TRACK_BLACKLIST)
        
        self.textual_blacklist = os.path.join(self.bundle, r'textual_blacklist' + CONTROL_EXT) # Costruisco il path del FILE TRACK BLACKLIST
        self.file_if_not(self.textual_blacklist, DEFAULT_TEXTUAL_BLACKLIST)

        self.sections_blacklist = os.path.join(self.bundle, r'sections_blacklist' + CONTROL_EXT) # Costruisco il path FILE SECTIONS BLACKLIST
        self.file_if_not(self.sections_blacklist, DEFAULT_SECTIONS_BLACKLIST)

        self.segments_blacklist = os.path.join(self.bundle, r'segments_blacklist' + CONTROL_EXT) # Costruisco il path del FILE SEGMENTS BLACKLIST 
        self.file_if_not(self.segments_blacklist, DEFAULT_SEGMENTS_BLACKLIST)
   
            
        # PRESETS
        self.weights_preset = os.path.join(self.presets, r'weights' +  DATAFRAME_EXT)
        self.csv_if_not(self.weights_preset, DEFAULT_WEIGHTS)
        
        
        
        
        
        
        
        
        
        