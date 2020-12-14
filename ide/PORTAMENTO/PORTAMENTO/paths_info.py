import os

# DEFAULT BLACKLISTS
DEFAULT_TRACK_BLACKLIST = "duration_ms\nloudness\nkey\nmode\npopularity\ntime_signature\n"
DEFAULT_SECTIONS_BLACKLIST = ""
DEFAULT_SEGMENTS_BLACKLIST = "loudness_end\n"
# ESTENSIONI BASE
CONTROL_EXT = ".txt"

class Path:
    
    songpack = []
    
    def __init__(self, base, bundle_name):    
        self.path_name = [                    
                        'sections',  #  - sezioni
                        'sections_confidences',  #  - sections_confidences
                        'segments',  #  - segmenti
                        'segments_confidences',  #  - segments_confidences
                        # 'segments_clust', #  - cluster segment
                        'n_songs']    #  - numero di canzoni  
        
        # CREO I PATH DI BASE
        self.bundles_path = os.path.join(base, r'bundles')
        if(not os.path.isdir(self.bundles_path)):
            os.mkdir(self.bundles_path)
        self.datasets_path = os.path.join(base, r'datasets')
        if(not os.path.isdir(self.datasets_path)):
            os.mkdir(self.datasets_path)
        
        self.bundle = os.path.join(self.bundles_path, bundle_name)    # Il path dal quale l'user può comandare gli input del software (playlist packs e blacklists)
        if(not os.path.isdir(self.bundle)):
            os.mkdir(self.bundle)
            
        self.dataset = os.path.join(self.datasets_path, bundle_name)  # Il path dei nostri dataset
        if(not os.path.isdir(self.dataset)):
            os.mkdir(self.dataset)
        
        
        # GLI UNICI FILE CHE CREO GIA' (E IL CUI PATH COMPRENDE L'ESTENSIONE) SON QUELLI CONTROLLABILI DALL'UTENTE NELLA CARTELLA BUNDLES
        #------------------------------------------------------------------------------------------------------------------------------
        self.oauth = os.path.join(base, r'oauth' + CONTROL_EXT)    # Costruisco il path del file dell'oauth token            
        #CREO IL FILE DELL'OAUTH
        if(not os.path.isfile(self.oauth)):
            crea = open(self.oauth, "w+")
            crea.close()
        
        self.playlistpack = os.path.join(self.bundle, bundle_name + CONTROL_EXT)    # Costruisco il path del file playlist_pack con tutti i link alle playlist
        #CREO IL FILE PLAYLISTPACK
        if(not os.path.isfile(self.playlistpack)):
           crea = open(self.playlistpack, "w+")
           crea.close()
        
        
        self.track_blacklist = os.path.join(self.bundle, r'track_blacklist' + CONTROL_EXT) # Costruisco il path del FILE TRACK BLACKLIST
        
        self.sections_blacklist = os.path.join(self.bundle, r'sections_blacklist' + CONTROL_EXT) # Costruisco il path FILE SECTIONS BLACKLIST
        
        self.segments_blacklist = os.path.join(self.bundle, r'segments_blacklist' + CONTROL_EXT) # Costruisco il path del FILE SEGMENTS BLACKLIST  
        
        # CREO I FILE BLACKLISTS
        if(not os.path.isfile(self.track_blacklist)):
            crea = open(self.track_blacklist, "w+")
            crea.write(DEFAULT_TRACK_BLACKLIST + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST.")
            crea.close()
        if(not os.path.isfile(self.sections_blacklist)):
            crea = open(self.sections_blacklist, "w+")
            crea.write(DEFAULT_SECTIONS_BLACKLIST + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST.")
            crea.close()
        if(not os.path.isfile(self.segments_blacklist)):
            crea = open(self.segments_blacklist, "w+")
            crea.write(DEFAULT_SEGMENTS_BLACKLIST + "FINE !!ATTENZIONE!!: NON TOCCARE QUESTA RIGA, SERVE A RICONOSCERE LA FINE DELLA BLACKLIST.")
            crea.close()
        
        
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
            if(not os.path.isdir(path)):
                os.mkdir(path)
        
        self.songpack[-1]['n_songs'] = os.path.join(playlist_path, r'n_songs')     # Costruisco il path del songpack del file songpack (il -1 è per aggiungere al dizionario appena messo nella lista)