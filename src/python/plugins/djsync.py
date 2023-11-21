# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 22:53:04 2021

@author: nicol
"""

# IMPORTO I PATHS
import paths_info

# IMPORTO DATASET UTILITIES
import datasets_utils as dt
import pandas as pd

# IMPORTO LE UTILITA' PER LE CANZONI
import posting as post

from datetime import datetime
import webbrowser

PLAYLIST_BASE_URL = "https://open.spotify.com/playlist/"

def main(bundle_name = "DJSYNC", FIRST_TIME = False, SAVE_DATASET = True, SAVE_FINAL_CLUSTERS = False, SONG_ANALYSIS_BOOL = False, CMD_LINE = True, user = r'nic'):
    
    # ************* INIZIO
    root = r'D:\PROJECTS\PORTAMENTO'
    paths = paths_info.Path(user, root)    # COLLEGO I PATH ALLE MIE STRUTTURE
    is_radar = False
    get_features_bool = False
    no_to_cross_playlist_duplicates = False
    PLAYLIST_PREFIX = ""
    
    paths.link_database(bundle_name)
    
    DEFAULT_ENABLED = False    # Bool per decidere se usare il valore di default FIRST_TIME
    if CMD_LINE and not DEFAULT_ENABLED:
        first_time = input("Nuovo caricamento? [(0)/1] - ")

        if first_time == '1':
            new_load = True
        else:
            first_time = False
    else: 
        first_time = FIRST_TIME
    
    # Carico il vecchio dataset
    if not first_time:
        new_load = False
        old = dt.Dataset(paths, is_radar, new_load, SAVE_DATASET, SONG_ANALYSIS_BOOL, get_features_bool, no_to_cross_playlist_duplicates)
        old_tracks = old.dataset['track']
        old_tracks = old_tracks.set_index('id')
        
        print("\nPlaylist attualmente in sync:\n")
        for playlist_name in set(old_tracks['playlist']):
            print(playlist_name)
    else:
        old_tracks = pd.DataFrame() # Dataframe vuoto
        
    if CMD_LINE:
        input("\nPuoi aggiornare gli uri delle playlist nel file in bundles/" + bundle_name + ", poi clicca invio. \n")
    
    # Poi lo riscarico
    paths.link_database(bundle_name)
    new_load = True
    new = dt.Dataset(paths, is_radar, new_load, SAVE_DATASET, SONG_ANALYSIS_BOOL, get_features_bool, no_to_cross_playlist_duplicates)
    new_tracks = new.dataset['track']
    new_tracks = new_tracks.set_index('id')
    
    # Controllo le differenze tramite gli indici presenti
    to_add = new_tracks[~new_tracks.index.isin(old_tracks.index)]
    to_delete = old_tracks[~old_tracks.index.isin(new_tracks.index)]
    
    paths.save_history(to_add, 'to_add')
    paths.save_history(to_delete, 'to_delete')
    
    to_add_playlists = []
    new_playlists = []
    if not to_add.empty:
        for playlist_id in set(to_add['playlist_id']):
            if old_tracks.empty:
                new_playlists.append(to_add.loc[to_add['playlist_id'] == playlist_id])
            elif playlist_id not in set(old_tracks['playlist_id']):
                new_playlists.append(to_add.loc[to_add['playlist_id'] == playlist_id])
            else:
                to_add_playlists.append(to_add.loc[to_add['playlist_id'] == playlist_id])
        
    to_delete_playlists = []
    if not to_delete.empty:
        for playlist_id in set(to_delete['playlist_id']):
            to_delete_playlists.append(to_delete.loc[to_delete['playlist_id'] == playlist_id])
    
 
    # Creo una playlist per le canzoni da aggiungere a ciascuna playlist
    now = datetime.now() # current date and time
    timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    print("\n")
    print("\nHo trovato canzoni da aggiungere in " + str(len(to_add_playlists)) + " playlist:\n\n")
    urls = ""
    for playlist in to_add_playlists:
        uris = "["
        count_sn = 0
        for uri in playlist['uri']:
            uris = uris + '"' + uri + '"' + ','
            count_sn = count_sn + 1
        uris = uris[:-1] + ']'
        new_playlist_id = post.create_playlist(PLAYLIST_PREFIX + playlist['playlist'][0], timestamp, uris, paths)
        playlist_url = PLAYLIST_BASE_URL + new_playlist_id
        webbrowser.open(playlist_url)
        urls = urls + playlist_url + "\n"
        print(str(count_sn) + " tracce da aggiungere a " + playlist['playlist'][0] + ";\n")
    
    print("--------------------------------")    
    print("\nHo trovato canzoni da eliminare in " + str(len(to_delete_playlists)) + " playlist:\n\n")
    for playlist in to_delete_playlists:
        print("\n" + playlist['playlist'][0] + ":\n")
        print(playlist[['name', 'artist', 'album']])
    
    print("--------------------------------")
    print("\nHo aggiunto al database le seguenti " + str(len(new_playlists)) + " playlist:\n\n")
    for playlist in new_playlists:
        print(playlist['playlist'][0] + "\n")
        playlist_url = PLAYLIST_BASE_URL + playlist['playlist_id'][0]
        urls = urls + playlist_url + "\n"
	
    print("--------------------------------")
    pd.DataFrame([urls]).to_clipboard(index = False, header = False)    # Li copio in clipboard
    print("Gli url delle playlist da scaricare sono stati copiati nella clipboard\n")
    input("Buon DJing!")
    
if __name__=="__main__":
    #main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], False)
    main()    # Per avvio dall'ide