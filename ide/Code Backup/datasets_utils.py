# IMPORTO LE UTILITA' PER LE CANZONI
import loading as load

# IMPORT GENERICHE
import copy

# PER GESTIRE I DATASET
import pandas as pd
import numpy as np

URI_LENGHT = 39  # Lunghezza dell'URI
URI_PORTION = 17    # Grandezza della prima porzione di uri (quella da cancellare)

# ESTENSIONI BASE
CONTROL_EXT = ".txt"
DATASET_EXT = ".csv"

class Dataset:
    
    dataset = {}
    
    def __init__(self, paths, new_load = 1):  # Costruisce un dizionario con all'interno i tre scope delle canzoni: vi son le coordinate per ogni canzone. Inoltre salvo in un file il numero di canzoni
        
        if(new_load):   # SE NON E' DA CARICARE LO CREIAMO DA ZERO
            
            dataset = {'track':[], 'track_confidences':[], 'sections':[], 'sections_confidences':[], 'segments':[], 'segments_confidences':[]}        
        
            count_pl = 0
            count_sn = 0
            
            #TODO : ottenere il nome della playlist e la songpack e utilizzare la richiesta di feature tutte insieme da una lista di canzoni
                    
            with open(paths.playlistpack, "r") as playlist_pack:
                for uri_pl in playlist_pack:
                    uri_pl = uri_pl[:URI_LENGHT]  # Questo serve a togliere il carattere in più (ossia '\n')
                    playlist_id = uri_pl[URI_PORTION:] # Taglio la porzione che ci serve, ossia l'ID
                    
                    print('\n' + str(count_pl + 1) + ': ')
                        
                    print('ID = ' + uri_pl + '\n')
                        
                    song_pack = load.get_songpack(playlist_id, paths)   # qui il path serve giusto per l'auth
                    
                    playlist_name = song_pack['name']
                    description = song_pack['description']
                    
                    features = load.get_features(song_pack, paths)  # qui il path serve giusto per l'auth
                    
                    dataset['track'].extend(features)
                    
                    paths.build_playlistpath(playlist_name)
    
                    for song_id in song_pack:
                        
                        print('\n' + str(count_sn + 1) + ': ')
                        
                        print('ID = ' + song_id + '\n')
                                
                        song = load.get_song_analysis(song_id, paths)    # Ottengo la canzone facendo la richiesta
                        
                        song['track']['playlist'] = playlist_name
                        song['track']['pl_description'] = description
                        
                        # space['track'] sarà una lista di dizionari ognuno con le coordinate di una canzone. Da una lista del genere è facile costruire un dataset.
                        dataset['track'].append(song['track'])     
                        dataset['track_confidences'].append(song['track_confidences'])
                                
                        # sections e segments non son più solo un dizionario: son liste di dizionari. L'approccio deve essere differente: space['sections'] sarà infatti una lista di liste di dizionari.
                        # Posso costruire il dataset su ogni singola canzone: questo dataset conterrà i segmenti/sezioni della canzone.
                        dataset['sections'].append(song['sections'])
                        dataset['sections_confidences'].append(song['sections_confidences'])
                        
                        dataset['segments'].append(song['segments'])
                        dataset['segments_confidences'].append(song['segments_confidences'])
                                
                        count_sn = count_sn + 1
                            
                    salva = open(paths.songpack[count_sn]['n_songs'] + ".txt", "w+")   # Salvo il numero delle canzoni
                    salva.write(str(count_sn))
                    salva.close()
                    
                    count_pl = count_pl + 1
                    playlist_pack.close()
                
                # POI LO CARICHIAMO. SE E' STATO APPENA CREATO SEMPLICEMENTE CARICHERA' CIO' CHE E' STATO APPENA CREATO
                
                self.load_dataset(paths)


    #************************************************************************************************************************************
    def save_dataset(self, dataset, paths):    # Trasforma ogni dizionario in un dataset e lo salva nella cartella corrispondente.
        
        print("Sto salvando il dataset.")
        
        for key in dataset:
            print('Salvo ' + key + '...')
            
            if 'track' in key:  # Le sezioni track e track_confidence del dataset son le uniche con un parametro per canzone.
                data = pd.DataFrame(dataset[key])   # La metto in un dataset
                salva = open(paths[key] + ".csv", "w+")
                export_csv = data.to_csv (paths[key] + ".csv", index = None, header=True)    # Esporto il dataset
                if str(export_csv) != 'None':
                        print("Errore salvando la parte Track.")
                salva.close()
            
            else:
                count = 0
                for song in dataset[key]:
                    data = pd.DataFrame(song)   # La metto in un dataset
                    salva = open(paths.__dict__[key] + r'\song' + str(count) + ".csv", "w+")
                    export_csv = data.to_csv (paths[key] + r'\song' + str(count) + ".csv", index = None, header=True)    # Esporto il dataset
                    if str(export_csv) != 'None':
                        print("Errore salvando " + key + " della canzone n. " + str(count))
                    salva.close()
                    count = count + 1

        return export_csv
    
    
    #************************************************************************************************************************************
    def load_dataset(self, paths):
        dataset = {}    # Il dataset non sarà altro in realtà che un dizionario di dataset:
        # 'n_song' è un semplice numero che indica il numero di canzoni nel dataset
        # 'track' contiene il dataset track
        # 'track_confidences' contiene il dataset track_confidence
        # 'sections' è una lista di dataset: un dataset per ogni canzone, contenente tutti le rispettive sections
        # 'segments' è una lista di dataset: un dataset per ogni canzone, contenente tutti i rispettivi segment
        # 'uris' e una lista degli uri di tutte le canzoni nel dataset.
        
        load = open(paths['n_songs'] + ".txt", "r")    # Carico il numero di canzoni
        dataset['n_songs'] = int(load.read())
        load.close()
        
        dataset['track'] = pd.read_csv(paths['track'] + ".csv")      # Caricamento del dataset track
        
        dataset['track_confidences'] = pd.read_csv(paths['track_confidences'] + ".csv")      # Caricamento del dataset track_confidences
        
        dataset['sections'] = [0] * dataset['n_songs']  # inizializzazione
        dataset['sections_confidences'] = [0] * dataset['n_songs']  # inizializzazione
        for i in range(dataset['n_songs']):     # Caricamento sezioni
            dataset['sections'][i] = pd.read_csv(paths['sections'] + r'\song' + str(i) + ".csv")
            dataset['sections_confidences'][i] = pd.read_csv(paths['sections_confidences'] + r'\song' + str(i) + ".csv")
            
        dataset['segments'] = [0] * dataset['n_songs']  # inizializzazione
        dataset['segments_confidences'] = [0] * dataset['n_songs']  # inizializzazione
        for i in range(dataset['n_songs']):     # Caricamento segmenti
            dataset['segments'][i] = pd.read_csv(paths['segments'] + r'\song' + str(i) + ".csv")
            dataset['segments_confidences'][i] = pd.read_csv(paths['segments_confidences'] + r'\song' + str(i) + ".csv")
        
        dataset['uris'] = [0] * dataset['n_songs']  # inizializzazione
        with open(paths['songpack'] + ".txt", "r") as song_pack:
            for i, uri in enumerate(song_pack):     # Caricamento uris
                dataset['uris'][i] = uri
        
       
        return split_dataset(dataset)
    
    
    #************************************************************************************************************************************
    def split_dataset(self, dataset):     # Divide il dataset in tre sezioni per organizzare meglio le cose
        
        split = { 'track':{}, 'sections':{}, 'segments':{} }
        
        for key in dataset:
            if 'track' in key:
                split['track'][key] = dataset[key]
            elif 'sections' in key:
                split['sections'][key] = dataset[key]
            elif 'segments' in key:
                split['segments'][key] = dataset[key]
            else:
                # Lo copio per evitare di avere referenze riguardo la stessa cosa in sezioni diversi: voglio poter modificare le cose in modo diverso per ogni sezione.
                split['track'][key] = copy.deepcopy(dataset[key])
                split['sections'][key] = copy.deepcopy(dataset[key])
                split['segments'][key] = copy.deepcopy(dataset[key])
        
        return split