import copy

# IMPORTO LE UTILITA' PER LE CANZONI
import loading as load

# PER SALVATAGGIO
import pickle

# PER GESTIRE I DATASET
import pandas as pd

URI_LENGHT = 39  # Lunghezza dell'URI
URI_PORTION = 17    # Grandezza della prima porzione di uri (quella da cancellare)

MAX_IDS_PER_REQUEST = 100 # Massimo numero di ids per feature request (imposto da spotify)


# ESTENSIONI BASE
CONTROL_EXT = ".txt"
DATASET_EXT = ".csv"

class Dataset:
    
    #*************************************** INIT
    def __init__(self, paths, is_radar = False, new_load = True, save_dataset = False, song_analysis_bool = False, get_features_bool = True, no_to_cross_playlist_duplicates = True):  # Costruisce un dizionario con all'interno i tre scope delle canzoni: vi son le coordinate per ogni canzone. Inoltre salvo in un file il numero di canzoni
        
        self.dataset = {}
        self.is_radar = is_radar
        self.save_dataset = save_dataset
        
        if(is_radar):
            dump_path = paths.radar_dump
        else:
            dump_path = paths.dataset_dump
        
        if(new_load):   # SE NON E' MAI STATO CREATO, LO CREIAMO DA ZERO E LO SALVIAMO
            self.get_and_save_dataset(paths, song_analysis_bool, get_features_bool, no_to_cross_playlist_duplicates)
            
            # NE FACCIO UN DUMP PER I PROSSIMI CARICAMENTI            
            with open(dump_path, "wb+") as salva:
                pickle.dump(self.dataset, salva)
            
        else:
            with open(dump_path, "rb") as file:
                self.dataset = pickle.load(file)

    #---------------------------
    def get_and_save_dataset(self, paths, song_analysis_bool = False, get_features_bool = True, no_to_cross_playlist_duplicates = True):  # Crea il dataset, e lo salva, creando i path di salvataggio
        
        dataset = {'track':[], 'track_confidences':[], 'sections':[], 'sections_confidences':[], 'segments':[], 'segments_confidences':[], 'artists':{}, 'albums':{}}
        
        count_pl = 0    #counter che si segna il numero di playlist
        total_songs = 0 #counter per tutte le canzoni del dataset
        
        if self.is_radar:
            playlistpack_path = paths.radarpack
            self.save_dataset = False    # Per assicurarmi che non venga salvato per errori nel chiamare la funzione
        else:
            playlistpack_path = paths.playlistpack
            
        with open(playlistpack_path, "r") as playlist_pack:
            for uri_pl in playlist_pack:
                count_sn = 0    #counter che si segna il numero di canzone
                
                uri_pl = uri_pl[:URI_LENGHT]  # Questo serve a togliere il carattere in più (ossia '\n')
                playlist_id = uri_pl[URI_PORTION:] # Taglio la porzione che ci serve, ossia l'ID
                
                print('\n' + str(count_pl + 1) + ': ')
                print('ID = ' + uri_pl)
                                
                # OTTENGO LA PLAYLIST
                playlist = load.get_playlist(playlist_id, paths)   # qui il path serve per l'auth
                playlist = self.format_playlist(playlist)
                
                song_pack = playlist['tracks']
                # OTTENGO LE FEATURES
                if get_features_bool:
                    features = load.get_features(song_pack, paths, 'first')  # qui il path serve per l'auth
                    features = self.format_features(features)
                
                    # Creo effettivamente il dataset
                    # dataset['track'] sarà una lista di dizionari ognuno con le coordinate di una canzone. Da una lista del genere è facile costruire un dataset.
                    dataset['track'].extend(features)
                    # sections e segments non son più solo un dizionario: son liste di dizionari. L'approccio deve essere differente: space['sections'] sarà infatti una lista di liste di dizionari.
                    # Posso costruire il dataset su ogni singola canzone: questo dataset conterrà i segmenti/sezioni della canzone.
                

                print(playlist['name'] + '\n')
                                

                for song in song_pack:
                    already_there = False
                    one_time = False
                    
                    # Aggiungo l'informazione di playlist_id
                    song['playlist_id'] = playlist_id
                    
                    if not get_features_bool:   # se avevamo le features l'abbiamo già aggiunta in bulk!
                        dataset['track'].append(song)
                    
                    ''' CONTROLLO SE C'E' GIA' '''
                    for track in dataset['track']:  # Due condizioni: una in cui non vogliamo i duplicati provenienti da playlist diverse, l'altra in cui li accettiamo ma eliminiamo comunque quelli nella stessa playlist.
                        if (no_to_cross_playlist_duplicates and song['id'] == track['id']) or (not no_to_cross_playlist_duplicates and song['id'] == track['id'] and playlist_id == track['playlist_id']):
                            if not one_time:    # Una volta ci sarà sempre perchè l'abbiamo aggiunta noi
                                one_time = True
                            else:    # SE E' PRESENTE PIU' DI UNA VOLTA
                                already_there = True
                                break
                               
                    if already_there:
                        if get_features_bool:   # Se non volevo le features, la canzone non è stata ancora aggiunta in ogni caso quindi non serve cancellarla
                            del dataset['track'][total_songs + count_sn] # Ossia cancello la riga che stavo componendo
                        continue    # salto questa iterazione ossia questa canzone
                    
                    # Aggiungo nome playlist alla struttura della canzone
                    song['playlist'] = playlist['name']
                    song['artist'] = song['artists'][0]['name']
                    song['artists_id'] = []
                    # Aggiungo gli artisti alla sezione del dataset e salvo solo gli id
                    for i, artist in enumerate(song['artists']):
                        song['artists_id'].append(artist['id'])
                        if(song['artists_id'][i] not in dataset['artists']):
                            dataset['artists'][song['artists_id'][i]] = song['artists'][i]
                    # Linearizzo la lista in una sola stringa separata da virgole. Per riottenere una lista posso fare my_string.split(",")
                    song['artists_id'] = " AND ".join(song['artists_id'])   # Lo faccio perchè semplifica la struttura e facilita la procedura di salvataggio
                    del song['artists']
                    
                    # Aggiungo l'album alla sezione del dataset e salvo solo l'id
                    song['album_id'] = song['album']['id']
                    if(song['album_id'] not in dataset['albums']):
                        dataset['albums'][song['album_id']] = song['album']
                    song['album'] = song['album']['name']
                        
                    # Aggiungo le nuove informazioni alla sezione track
                    dataset['track'][total_songs + count_sn].update(song)
                    
                    # ANALISI AGGIUNTIVE E ACCURACIES:
                    if(song_analysis_bool == True and already_there == False):
                        song_id = song['id']
                        
                        print('\n' + str(count_sn + 1) + ': ')
                        print(song['name'] + " - ID: " + song_id + '\n')
                        
                        # Ottengo l'analisi facendo la richiesta
                        analysis = load.get_song_analysis(song_id, paths)
                        analysis = self.format_analysis(analysis)
                        

                        # La sezione track è già stata popolata attraverso le features. Popoliamo la sezione delle confidenze
                        dataset['track_confidences'].append(analysis['track']) # La sezione track delle analisi contiene solo confidenze dopo la formattazione
                        del analysis['track']  # La cancello perchè non mi serve più e facilita il salvataggio
                        
                        # Infine popoliamo sezioni e segmenti del dataset con le loro confidenze
                        dataset['sections'].append(analysis['sections'])
                        dataset['sections_confidences'].append(analysis['sections_confidences'])
                        dataset['segments'].append(analysis['segments'])
                        dataset['segments_confidences'].append(analysis['segments_confidences'])
                        
                        
                        # -------------- SALVATAGGIO
                        # Salvo i dataset creati
                        if self.save_dataset:
                            self.save_analysis(analysis, count_pl, count_sn, paths)
                    #-------------------------------------------------------------------- FINE DELL'IF
                        
                    # Aggiorno l'iteratore delle canzoni
                    count_sn = count_sn + 1
                    # ------------------------------------...FINE FOR DELLE CANZONI
                
                total_songs = total_songs + count_sn
                
                
                
                # ---------- SALVATAGGIO
                # Salvo il numero delle canzoni della playlist
                if self.save_dataset:
                    self.save_n_songs(count_pl, count_sn, paths)
                    paths.save_playlist_name(count_pl, playlist['name'], "https://open.spotify.com/playlist/" + playlist_id)
                
                
                
                # Aggiorno l'iteratore delle playlist                
                count_pl = count_pl + 1
                #----------------------------------------------- FINE FOR DELLE PLAYLIST
            
            
            # SALVATAGGI FINALI
        if(song_analysis_bool):
            self.save_dataset_key(dataset, 'track_confidences', paths)  # la ho solo se ho fatto l'analisi
        
        if self.save_dataset:
            self.save_dataset_key(dataset, 'track', paths)
            self.save_dataset_key(dataset, 'albums', paths)
            self.save_dataset_key(dataset, 'artists', paths)
            self.save_n_playlists(count_pl, paths)
        
        self.dataset['track'] = pd.DataFrame(dataset['track'])
        self.dataset['original_track'] = copy.deepcopy(self.dataset['track'])   # La sezione track verrà modificata nel clustering
        self.dataset['albums'] = pd.DataFrame(dataset['albums'])
        self.dataset['artists'] = pd.DataFrame(dataset['artists'])
        
        
    #************************************************************************************************************************************
    def save_dataset_key(self, dataset, key, paths):    # Trasforma i dizionari delle sezioni track e track_confidences in un dataset e li salva nella cartella corrispondente.
        
        to_save = dataset[key]
        
        print("Sto salvando la sezione " + key + " del dataset.")
        
        data = pd.DataFrame(to_save)   # La metto in un dataset
        salva = open(paths.__dict__[key] + ".csv", "w+")
        export_csv = data.to_csv (paths.__dict__[key] + ".csv", index = None, header=True)    # Esporto il dataset
        if str(export_csv) != 'None':
            print("Errore salvando la parte " + key + ".")
        salva.close()                

        return export_csv

    #-------------
    def save_analysis(self, analysis, playlist_num, song_num, paths):    # Trasforma i dizionari delle sezioni sections, segments e rispettive accuracies (per ogni canzone) in un dataset e li salva nella cartella corrispondente.

        for key in analysis:
            data = pd.DataFrame(analysis[key])   # La metto in un dataset
            salva = open(paths.songpack[playlist_num][key] + r'\song' + str(song_num) + ".csv", "w+")
            export_csv = data.to_csv (paths.songpack[playlist_num][key] + r'\song' + str(song_num) + ".csv", index = None, header=True)    # Esporto il dataset
            if str(export_csv) != 'None':
                print("Errore salvando " + key + " della canzone n. " + str(song_num))
            salva.close()

        return export_csv
    
    #-------------
    def save_n_songs(self, numero_playlist, n_songs, paths):
        salva = open(paths.songpack[numero_playlist]['n_songs'] + ".txt", "w+")   
        salva.write(str(n_songs))
        salva.close()
        
    def save_n_playlists(self, n_playlists, paths):
        salva = open(paths.n_playlists + ".txt", "w+")   
        salva.write(str(n_playlists))
        salva.close()
           
    
    #************************************************************************************************************************************
    def format_analysis(self, song):
    
        # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
        del song['track']['analysis_channels']
        del song['track']['analysis_sample_rate']
        del song['track']['code_version']
        del song['track']['codestring']
        del song['track']['duration']
        del song['track']['echoprint_version']
        del song['track']['echoprintstring']
        del song['track']['end_of_fade_in']
        
        del song['track']['num_samples']
        del song['track']['offset_seconds']
        del song['track']['rhythm_version']
        del song['track']['rhythmstring']
        del song['track']['sample_md5']
        del song['track']['start_of_fade_out']
        del song['track']['synch_version']
        del song['track']['synchstring']
        del song['track']['window_seconds']
        
        # Elimino parametri che ho già ottenuto tramite la richiesta di features
        del song['track']['key']
        del song['track']['loudness']
        del song['track']['mode']
        del song['track']['tempo']
        del song['track']['time_signature']
        # LA SEZIONE track DELLA CANZONE ORA CONTIENE DI FATTO SOLO LE CONFIDENZE DI ALCUNI PARAMETRI OTTENUTI TRAMITE LE FEATURES.
    
        del song['meta']
        del song['bars']
        del song['beats']
        del song['tatums']
    
        for segment in song['segments']:
            # Elimino un campo che non ci interessa
            del segment['start']
         
            # Rendo lineari i segmenti
            for i in range(len(segment['pitches'])):
                segment['pitch' + str(i)] = segment['pitches'][i]
            del segment['pitches']
            for i in range(len(segment['timbre'])):
                segment['timbre' + str(i)] = segment['timbre'][i]
            del segment['timbre']
        
        
        # SEPARO LE CONFIDENZE DAI VALORI:
            
            # SECTIONS:
        # creo il campo per le confidenze
        song['sections_confidences'] = []
        count = 0
        # Separo le confidenze delle sezioni dai valori delle sezioni
        for section in song['sections']:
            song['sections_confidences'].append({key:section[key] for key in section if 'confidence' in key})
            song['sections'][count] = {key:section[key] for key in section if 'confidence' not in key}
            count = count + 1
        
            # SEGMENTS:
        # creo il campo per le confidenze
        song['segments_confidences'] = []
        count = 0
        # Separo le confidenze dei segmenti dai valori dei segmenti
        for segment in song['segments']:
            song['segments_confidences'].append({key:segment[key] for key in segment if 'confidence' in key})
            song['segments'][count] = {key:segment[key] for key in segment if 'confidence' not in key}
            count = count + 1
        
        # Avremo diviso ora il dizionario song in 4 keys: Track con informazioni generali sul sound della traccia, Segments con informazioni 
        # precise sui singoli suoni della traccia, Sections con informazioni sul sound di sezioni più grosse della traccia.
        # Avremo dunque 3 scope di precisione diversa.
        # C'è inoltre la key dell'ID in cui c'è semplicemente l'identificativo della traccia, che può essere visto come la precisione massima
        
        return song
    
      
    #-------------    
    def format_playlist(self, playlist):
        # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
        
        del playlist['collaborative']
        del playlist['description']
        del playlist['external_urls']
        del playlist['followers']
        del playlist['href']
        del playlist['id']
        del playlist['images']
        del playlist['owner']
        del playlist['public']
        del playlist['snapshot_id']
        del playlist['type']
        del playlist['uri']
        del playlist['primary_color']
    
        playlist['tracks'] = playlist['tracks']['items']
        
        to_delete = []
        for i, item in enumerate(playlist['tracks']):
            item = item['track']
            if item['id'] is None:
                to_delete.append(i)
            else:
                del item['available_markets']
                del item['duration_ms']
                del item['episode']
                del item['external_ids']
                del item['external_urls']
                del item['explicit']
                del item['type']
                del item['href']
                del item['track']
                del item['is_local']
                playlist['tracks'][i] = item
        
        for i in to_delete:
            del playlist['tracks'][i]
        return playlist
            
    #---------------
    def format_features(self, features):
    # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
    
        for song in features:
        
            del song['type']
            del song['analysis_url']
            del song['uri']
            del song['track_href']
        
        return features