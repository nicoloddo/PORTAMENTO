# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 18:27:11 2021

@author: nicol
"""

# IMPORTO LE UTILITA' PER LE CANZONI
import loading as load

import pandas as pd

URI_LENGHT = 39  # Lunghezza dell'URI
URI_PORTION = 17    # Grandezza della prima porzione di uri (quella da cancellare)

class Playlist_compass:
    
    def __init__(self, paths, uri_pl):
        
        uri_pl = uri_pl[:URI_LENGHT]  # Questo serve a togliere il carattere in più (ossia '\n')
        playlist_id = uri_pl[URI_PORTION:] # Taglio la porzione che ci serve, ossia l'ID
        
        print('ID = ' + uri_pl)
        
        # OTTENGO LA PLAYLIST
        playlist = load.get_playlist(playlist_id, paths)   # qui il path serve per l'auth
        playlist = self.format_playlist(playlist)
        
        song_pack = playlist['tracks']
        # OTTENGO LE FEATURES
        self.features = load.get_features(song_pack, paths)  # qui il path serve per l'auth
        self.features = self.format_features(self.features)
        
        # AGGIUNGO ALTRE INFORMAZIONI UTILI
        for i, song in enumerate(song_pack):
            self.features[i].update(song)
        
        # IMPACCHETTO
        self.features = pd.DataFrame(self.features)
        
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
    
        for i, item in enumerate(playlist['tracks']):
            item = item['track']
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
        
        return playlist

    #-------------
    def format_features(self, features):
    # Rimuovo cose di cui non so che farmene o che trovo inutili per i miei scopi, anche per semplificare la struttura
    
        for song in features:
        
            del song['type']
            del song['analysis_url']
            del song['uri']
            del song['track_href']
        
        return features